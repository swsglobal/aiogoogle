import pytest

import pprint
from aiogoogle import DiscoveryClient
from aiogoogle.resource import Resource, Resources
from aiogoogle.method import ResourceMethod
from ...globals import SOME_APIS

@pytest.mark.parametrize('name,version', SOME_APIS)
def test_resource_constructor(open_discovery_document, name, version):
    discovery_document = open_discovery_document(name, version)
    client = DiscoveryClient(discovery_document=discovery_document)
    for resource_name, _ in discovery_document.get('resources').items():
        resource_object = getattr(client.resources, resource_name)
        assert isinstance(resource_object, Resource)
        assert resource_name == resource_object.name
        assert resource_object._resource_specs == discovery_document['resources'][resource_name]
        assert resource_object._global_parameters == discovery_document.get('parameters')
        assert resource_object._schemas == discovery_document.get('schemas')
        ##
        assert client.resources._schemas is resource_object._schemas
        assert client.resources._global_parameters is resource_object._global_parameters

def test_resources_property():
    resource = Resource(
        name='irrelevant',
        resource_specs={
            'resources': {
                'first_resource': 1,
                'second_resource': 2
            },
            'methods': {
                'third_method': 3,
                'forth_method': 4
            }
        },
        global_parameters = None,
        schemas = None,
        base_url = None,
        root_url = None,
        validate = False
    )
    assert 'first_resource' in resource.resources
    assert 'second_resource' in resource.resources

def test_methods_property():
    resource = Resource(
        name='irrelevant',
        resource_specs={
            'resources': {
                'first_resource': 1,
                'second_resource': 2
            },
            'methods': {
                'third_method': 3,
                'forth_method': 4
            }
        },
        global_parameters = None,
        schemas = None,
        base_url = None,
        root_url = None,
        validate = False
    )
    assert 'third_method' in resource.methods
    assert 'forth_method' in resource.methods

def test_resource_len():
    resource = Resource(
        name='irrelevant',
        resource_specs={
            'resources': {
                'first_resource': 1,
                'second_resource': 2,
                'basdasd': 239
            },
            'methods': {
                'third_method': 3,
                'forth_method': 4
            }
        },
        global_parameters = None,
        schemas = None,
        base_url = None,
        root_url = None,
        validate = False
    )
    assert len(resource) == 2

@pytest.mark.parametrize('name,version', SOME_APIS)
def test_resource_returns_nested_resource(open_discovery_document, name, version):
    discovery_document = open_discovery_document(name, version)
    client = DiscoveryClient(discovery_document=discovery_document)
    for resource_name, _ in discovery_document.get('resources', {}).items():
        resource = getattr(client.resources, resource_name)
        if resource.resources:
            # Assert that it returns resources not methods
            for nested_resource_name in resource.resources:
                nested_resource = getattr(resource, nested_resource_name)
                assert isinstance(nested_resource, Resource)

@pytest.mark.parametrize('name,version', SOME_APIS)
def test_resource_returns_available_methods(open_discovery_document, name, version):
    discovery_document = open_discovery_document(name, version)
    client = DiscoveryClient(discovery_document=discovery_document)
    for resource_name, _ in discovery_document.get('resources', {}).items():
        resource = getattr(client.resources, resource_name)
        if resource.methods:
            # Assert that it returns resources not methods
            for available_method_name in resource.methods:
                available_method = getattr(resource, available_method_name)
                assert isinstance(available_method, ResourceMethod)


@pytest.mark.parametrize('name,version', SOME_APIS)
def test_method_construction(open_discovery_document, name, version):
    discovery_document = open_discovery_document(name, version)
    client = DiscoveryClient(discovery_document=discovery_document)
    for resource_name, _ in discovery_document.get('resources').items():
        resource = getattr(client.resources, resource_name)
        for method_name in resource.methods:
            resource_method = getattr(resource, method_name)
            # Assert a resource has the returned method
            assert resource_method.name in discovery_document['resources'][resource_name]['methods']
            # Assert specs belong to the created method
            assert resource_method._method_specs == discovery_document['resources'][resource_name]['methods'][method_name]
            # Assert global parameters were passed correctly
            assert resource_method._global_parameters == discovery_document.get('parameters')
            # Assert schemas where passed correctly
            assert resource_method._schemas == discovery_document.get('schemas')

@pytest.mark.parametrize('name,version', SOME_APIS)
def test_resource_construction(open_discovery_document, name, version):
    discovery_document = open_discovery_document(name, version)
    client = DiscoveryClient(discovery_document=discovery_document)
    for resource_name, _ in discovery_document.get('resources').items():
        resource = getattr(client.resources, resource_name)
        for nested_resource_name in resource.resources:
            nested_resource = getattr(resource, nested_resource_name)
            assert isinstance(nested_resource, Resource)

@pytest.mark.parametrize('name,version', SOME_APIS)
def test_calling_resource_fails(open_discovery_document, name, version):
    discovery_document = open_discovery_document(name, version)
    client = DiscoveryClient(discovery_document=discovery_document)
    for resource_name, _ in discovery_document.get('resources').items():
        resource = getattr(client.resources, resource_name)
        with pytest.raises(TypeError):
            resource()

@pytest.mark.parametrize('name,version', SOME_APIS)
def test_str_resource(open_discovery_document, name, version):
    discovery_document = open_discovery_document(name, version)
    client = DiscoveryClient(discovery_document=discovery_document)
    for resource_name, _ in discovery_document.get('resources').items():
        resource = getattr(client.resources, resource_name)
        assert discovery_document['baseUrl'] in str(resource)
        assert 'resource' in str(resource)