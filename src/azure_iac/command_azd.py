import os
import sys
sys.path.append(os.path.abspath('../'))
import json
from azure_iac.payloads.payload import Payload
from azure_iac.generators.bicep_generator import BicepGenerator
from azure_iac.generators.azure_yaml_generator import AzureYamlGenerator
from azure_iac.generators.dot_env_generator import DotEnvGenerator


class CommandAzd:
    def __init__(self):
        pass

    def execute(self, payload_path='../../test.payload.json', output_path='../../output'):
        content = open(payload_path, 'r').read()
        input_json = json.loads(content)
        input_json['projectType'] = 'azd'
        payload = Payload.from_json(input_json)
    
        bicep_generator = BicepGenerator(payload)
        bicep_generator.generate(output_path+'/infra')

        azure_yaml_generator = AzureYamlGenerator(payload)
        azure_yaml_generator.generate(output_path)

        dot_env_generator = DotEnvGenerator(payload)
        dot_env_generator.generate(output_path)


def main():
    command = CommandAzd()
    if len(sys.argv) > 2:
        command.execute(
            payload_path = sys.argv[1], 
            output_path = sys.argv[2])
    else:
        from colorama import Fore, Style
        print(Fore.YELLOW + '''Please run command with correct syntax: 
              ./generator.exe <your-payload>.json <your-output-folder>''' + Style.RESET_ALL)


if __name__ == '__main__':
    main()