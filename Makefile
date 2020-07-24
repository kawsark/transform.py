setup_azure:
	vault write transform/template/azure-template type=regex \
		pattern="([a-z0-9]+)-([a-z0-9]+)-([a-z0-9]+)-([a-z0-9]+)-([a-z0-9]+)" \
		alphabet=builtin/alphanumericlower
	
	vault write transform/template/azure-client-secret-template type=regex \
		pattern="([A-Za-z0-9]+)" \
		alphabet=builtin/alphanumeric

setup_azure_fpe: setup_azure
	vault delete transform/role/azure-role
	vault delete transform/transformation/azure
	vault delete transform/transformation/azure-client-secret

	vault write transform/transformation/azure \
        type=fpe \
        template=azure_template \
        tweak_source=internal \
        allowed_roles='azure-role'
	
	vault write transform/transformation/azure-client-secret \
        type=fpe \
        template=azure-client-secret-template \
        tweak_source=internal \
        allowed_roles='azure-role'

	vault write transform/role/azure-role transformations=azure,azure-client-secret

setup_azure_masking: setup_azure
	vault delete transform/role/azure-role
	vault delete transform/transformation/azure
	vault write transform/transformation/azure \
        type=masking \
        template=azure_template \
		masking_character='#' \
        allowed_roles='azure-role'

	vault write transform/role/azure-role transformations=azure

setup_aws:
	vault write transform/alphabet/aws_creds alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+/"
	vault write transform/template/aws_template type=regex \
		pattern="([A-Za-z0-9/\+]+)" \
		alphabet=aws_creds
	
setup_aws_fpe: setup_aws
	vault delete transform/role/aws-role
	vault delete transform/transformation/aws
	vault write transform/transformation/aws \
		type=fpe \
		template=aws_template \
		tweak_source=internal \
		allowed_roles='aws-role'

	vault write transform/role/aws-role transformations=aws


setup_aws_masking: setup_aws
	vault delete transform/role/aws-role
	vault delete transform/transformation/aws

	vault write transform/transformation/aws \
		type=masking \
		template=aws_template \
		masking_character='#' \
		allowed_roles='aws-role'

	vault write transform/role/aws-role transformations=aws