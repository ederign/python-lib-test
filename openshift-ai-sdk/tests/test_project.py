import pytest
from openshift_ai_sdk.project import Project  # Adjust the import path as needed

@pytest.fixture(autouse=True)
def clean_projects_dictionary():
    Project.projects = {}
    yield

def test_project_creation():
    project = Project.create('TestProject', 'TestResource', 'Test description')
    assert isinstance(project, Project), "The created object should be an instance of Project"
    assert project.name == 'TestProject'
    assert project.resource_name == 'TestResource'
    assert project.description == 'Test description'
    assert Project.projects['TestProject'] == project

def test_project_read():
    Project.create('TestProject', 'TestResource', 'Test description')
    project = Project.read('TestProject')
    assert isinstance(project, Project), "The read object should be an instance of Project"
    assert project.name == 'TestProject'

def test_project_update():
    Project.create('TestProject', 'TestResource', 'Test description')
    project = Project.update('TestProject', description='Updated description')
    assert isinstance(project, Project), "The updated object should be an instance of Project"
    assert project.description == 'Updated description'

def test_project_delete():
    Project.create('TestProject', 'TestResource', 'Test description')
    delete_message = Project.delete('TestProject')
    assert delete_message == "Project 'TestProject' deleted."
    assert 'TestProject' not in Project.projects

def test_project_not_found_on_read():
    project = Project.read('Nonexistent')
    assert project is None, "Reading a non-existent project should return None"

def test_project_not_found_on_update():
    project = Project.update('Nonexistent', description='Should not update')
    assert project is None, "Updating a non-existent project should return None"

def test_project_duplicate_creation():
    Project.create('TestProject', 'TestResource', 'Test description')
    with pytest.raises(ValueError) as excinfo:
        Project.create('TestProject', 'TestResource', 'Another description')
    assert "Project with this name already exists." in str(excinfo.value)
