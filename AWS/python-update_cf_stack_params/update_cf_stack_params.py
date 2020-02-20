import logging
import boto3
import argparse
import ast


class CfUpdateParams():
    cf = None

    def __init__(self, region):
        self.cf = boto3.client('cloudformation', region)

    def get_stack_default_params(self, stack_name):
        try:
            response = self.cf.describe_stacks(
                StackName=stack_name
            )
        except Exception as error_msg:
            logging.error(error_msg)
            raise Exception("method: describe_stack - {}".format(error_msg))
        logging.info("Get stack {} previous param values".format(stack_name))
        return response['Stacks'][0]['Parameters']

    def validate_params(self, valid_params_list, params_to_validate):
        try:
            params_to_validate_keys_list = []
            for param_to_validate in params_to_validate:
                params_to_validate_keys_list.append(param_to_validate['ParameterKey'])

            valid_params_keys_list = []
            for valid_param in valid_params_list:
                valid_params_keys_list.append(valid_param['ParameterKey'])

            cross_keys_list = [key_name for key_name in params_to_validate_keys_list if key_name in valid_params_keys_list]
            if cross_keys_list == params_to_validate_keys_list:
                logging.info("Stack params validated")
                return True

            raise Exception("\"{}\" is/are not a valid param".format([key_name for key_name in params_to_validate_keys_list if key_name not in cross_keys_list]))

        except Exception as error_msg:
            logging.error(error_msg)
            raise Exception("method: validate_param - {}".format(error_msg))

    def build_params(self, default_params, params_to_update):
        try:
            for param_to_update in params_to_update:
                index = 0
                for default_param in default_params:
                    if param_to_update['ParameterKey'] == default_param['ParameterKey']:
                        default_params.pop(index)
                        break
                    index += 1
            updated_params = params_to_update + default_params
            logging.info("New params build successful")
            return updated_params
        except Exception as error_msg:
            logging.error(error_msg)
            raise Exception("method: build_params - {}".format(error_msg))

    def update_stack(self, stack_name, list_of_params):
        try:
            self.cf.update_stack(
                StackName=stack_name,
                UsePreviousTemplate=True,
                Parameters=list_of_params,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            self.cf.get_waiter('stack_update_complete').wait(
                StackName=stack_name,
            )
            logging.info("Stack {} params updated successfully".format(stack_name))

        except Exception as error_msg:
            logging.error(error_msg)
            raise Exception("method: update_stack - {}".format(error_msg))


def main():
    try:
        # Set logging
        logging.basicConfig(level=logging.INFO)
        logging.info("Loading config from yaml file")

        # Load/Parse Arg params
        parser = argparse.ArgumentParser()
        required = parser.add_argument_group('required arguments')
        required.add_argument("--region", required=True, type=str, help="AWS Stack region")
        required.add_argument("--stack_name", required=True, type=str, help="AWS Stack name")
        required.add_argument("--params_list", required=True, type=ast.literal_eval, help="""
        List of parameters to update. The parameter format is as following:
        --params_list "[{'ParameterKey': 'Param_1_Key', 'ParameterValue': 'Param_1_Value'}, {'ParameterKey': 'Param_2_Key', 'ParameterValue': 'Param_2_Value'}...]"
        """)
        args = parser.parse_args()

        cf_stack = CfUpdateParams(region=args.region)
        cf_stack_default_params = cf_stack.get_stack_default_params(stack_name=args.stack_name)
        cf_stack.validate_params(valid_params_list=cf_stack_default_params, params_to_validate=args.params_list)
        cf_stack_update_params = cf_stack.build_params(default_params=cf_stack_default_params, params_to_update=args.params_list)
        cf_stack.update_stack(stack_name=args.stack_name, list_of_params=cf_stack_update_params)

    except Exception as error_msg:
        raise Exception("Error - Something bad happened - {}.".format(error_msg))


# main entry point
if __name__ == "__main__":
    main()
