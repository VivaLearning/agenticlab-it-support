# Configurazione Azure OpenAI
Questa procedura riproduce il deployment utilizzato nel collaudo iniziale. Modelli, disponibilità e quota dipendono dalla sottoscrizione. I nomi delle risorse devono essere disponibili globalmente. Il deployment a consumo genera costi quando viene invocato.
## 1. Autenticazione
```powershell
az login --use-device-code
az account list -o table
az account set --subscription "SUBSCRIPTION_ID"
az account show -o table
```
In caso di identità duplicate, az logout e az account clear, poi az login --use-device-code --tenant "TENANT_ID". Questi comandi cancellano le sessioni locali CLI, non risorse Azure.
## 2. Resource group e risorsa
```powershell
az group create --name rg_poc_agentico --location swedencentral -o table
az cognitiveservices account create --name aoai-vivalearning-agenticlab --resource-group rg_poc_agentico --location swedencentral --kind OpenAI --sku S0 --custom-domain aoai-vivalearning-agenticlab --yes -o table
az cognitiveservices account show --name aoai-vivalearning-agenticlab --resource-group rg_poc_agentico --query "{State:properties.provisioningState,Endpoint:properties.endpoint}" -o table
```
Se il nome è occupato, sceglierne uno univoco e sostituirlo nei comandi successivi. Se si dispone già di una risorsa compatibile, riutilizzarla.
## 3. Modello e quota
```powershell
az cognitiveservices account list-models --name aoai-vivalearning-agenticlab --resource-group rg_poc_agentico --query "[?name=='gpt-4.1-mini'].{Model:name,Version:version,SKUs:skus}" -o json
az cognitiveservices usage list --location swedencentral --query "[?name.value=='OpenAI.GlobalStandard.gpt4.1-mini'].{Name:name.value,Current:currentValue,Limit:limit}" -o table
```
Il POC è stato configurato con GPT-4.1-mini versione 2025-04-14, GlobalStandard, capacità 50 (50.000 TPM secondo la quota restituita nel collaudo). Verificare disponibilità e quota prima della creazione.
```powershell
az cognitiveservices account deployment create --name aoai-vivalearning-agenticlab --resource-group rg_poc_agentico --deployment-name agenticlab-model --model-name gpt-4.1-mini --model-version 2025-04-14 --model-format OpenAI --sku-name GlobalStandard --sku-capacity 50 -o table
az cognitiveservices account deployment show --name aoai-vivalearning-agenticlab --resource-group rg_poc_agentico --deployment-name agenticlab-model --query "{Deployment:name,Model:properties.model.name,State:properties.provisioningState,SKU:sku.name,Capacity:sku.capacity}" -o table
```
## 4. RBAC
```powershell
$resourceId = az cognitiveservices account show --name aoai-vivalearning-agenticlab --resource-group rg_poc_agentico --query id -o tsv
$userId = az ad signed-in-user show --query id -o tsv
az role assignment create --assignee-object-id $userId --assignee-principal-type User --role "Cognitive Services OpenAI User" --scope $resourceId -o table
az role assignment list --assignee $userId --scope $resourceId --include-inherited --query "[].{Role:roleDefinitionName,Scope:scope}" -o table
```
Occorrono permessi per assegnare ruoli. Attendere la propagazione RBAC in caso di 403. DefaultAzureCredential usa una catena di credenziali, non necessariamente Azure CLI se altre credenziali sono disponibili.
## 5. Configurazione .env e smoke test
Inserire endpoint effettivo, deployment agenticlab-model e API version 2024-10-21 (configurazione collaudata). Non usare chiavi API.
```powershell
.\.venv\Scripts\python.exe -c "from dotenv import load_dotenv; load_dotenv(); from backend.llm import call; result, tokens = call('planner', [{'role':'user','content':'Presentati brevemente senza utilizzare strumenti.'}], 1000); print(result); print('Tokens:', tokens)"
.\.venv\Scripts\python.exe -c "from dotenv import load_dotenv; load_dotenv(); from backend.llm import call; result, tokens = call('planner', [{'role':'user','content':'Consulta la knowledge base utilizzando lo strumento disponibile.'}], 1000); print(result); print('Tokens:', tokens)"
```
Il secondo comando dovrebbe produrre tool_calls con knowledge; il modello non è obbligato a farlo. Non esegue ancora il tool. La dashboard esegue il ciclo completo.
## 6. Costi e dismissione
MAX_TOKENS è una soglia applicativa tra chiamate, non un limite di spesa Azure. La capacità TPM è throughput, non consumo acquistato. Consultare prezzi e monitoraggio Azure per costi effettivi. Al termine, eliminare il deployment o il resource group dedicato soltanto dopo aver verificato che nessun altro progetto lo utilizzi. Non cancellare risorse condivise.
