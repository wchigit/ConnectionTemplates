def get_kebal(name: str):
    return name.replace('_', '-').lower()

def get_pascal(name: str):
    return ''.join([word.capitalize() for word in name.split('-')])

def get_camel(s: str):
    words = s.split('-')
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def format_module_name(default_name: str, instance_name: str):
    instance_name = '' if instance_name == None else instance_name
    return '{}{}Deployment'.format(default_name, get_pascal(instance_name))

def format_deployment_name(default_name: str, instance_name: str):
    instance_name = '' if instance_name == None else instance_name
    return '{}-{}-deployment'.format(get_kebal(default_name), get_kebal(instance_name))

def format_kv_secret_name(default_name: str, instance_name: str):
    instance_name = '' if instance_name == None else instance_name
    return '{}-{}-secret'.format(get_kebal(default_name), get_kebal(instance_name))


def format_camel(*args):
    return args[0] + ''.join(word.capitalize() for word in args[1:])

def format_snake(*args):
    return '_'.join([word.lower() for word in args if word])

def format_resource_name(prefix: str):
    return prefix[-6:] + '${resourceToken}'

def get_location():
    return 'resourceGroup().location'

def get_random_str(length: int):
    import random
    import string

    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(length)).lower()

