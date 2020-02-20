# AWS update cloudformation stack parameters

This script will update a stack specified parameters and keep/use the previously defined values for the other parameters.  

## Prerequisites
* Install prerequisites by running the below commands:
```bash
# Optional - Install and load Virtualenv
pip3 install virtualenv
virtualenv env
source env/bin/activate
# Install Requirements
pip3 install -r requirements.txt
```

## Usage:
* Run the command below:
```bash
python3 update_cf_stack_params.py --region eu-west-1 --params_list "[{'ParameterKey':'Param_1_Key', 'ParameterValue': 'Param_1_Value'}, {'ParameterKey': 'Param_2_Key', 'ParameterValue':'Param_2_Value'}...]" --stack_name "YOUR_STACK_NAME"
```

## Github related issue:
[aws-cli - issue 2589](https://github.com/aws/aws-cli/issues/2589)
