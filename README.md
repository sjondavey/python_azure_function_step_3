# python_azure_function_step_3

In Step 3, I add Azure Blob Triggers and Storage to the existing [HTTP triggered, Python based Azure Function](https://github.com/sjondavey/python_azure_function_step_2) applying techniques from Microsoft's documentation [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-storage-queue-vs-code?pivots=programming-language-python), and [here](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-07). The first part will focus on using Azure and the second part will use [Azurite](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azurite) for local development and testing of the Blog trigger.

There are a few other references that are worth looking at:
1. [Azure Functions and Blob Storage](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-storage-blob-triggered-function). This is not Python specific but is useful
2. [Worked example using Blob Storage Trigger](https://github.com/yokawasa/azure-functions-python-samples/tree/master/v2functions/blob-trigger-cosmosdb-out-binding#create-blob-storage-account--container)

### Add Blob Trigger Endpoints
It is easier to start with the Azure Development (as opposed to local development using the Azurite storage emulator) which means starting with a clean copy of the code from Step 2. Make sure you have installed the Azure Storage Extension for VSCode. It is not necessary to install Azure Storage Explorer at this stage (you need it when using Azurite for local development or testing) as you can interact with your storage account in the Azure Portal. 

Starting from Step 2, use the Azure Extension (`ctrl+shft+A`) to `Create Function` / `Azure Blob Storage Trigger` I will call my endpoint `simulateEquityPortfolioBlob`. Use `AzureWebJobsStorage` settings and the default `samples-workitems/{name}` path for the trigger. Now `Deploy to Function App`. Once the app is deployed, you need to [get the settings](https://docs.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-storage-queue-vs-code?pivots=programming-language-python#download-the-function-app-settings) and [add an out binding](https://docs.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-storage-queue-vs-code?pivots=programming-language-python#add-an-output-binding) to Azure Blob Storage. Leave the path as the default `outcontainer/{rand-guid}` 

**Note: Blob Filenames** `functions.json` contains 'bindings' between the Function and it's inputs and outputs. Bindings are easy but are limited. For more control you need to use the [Azure Storage SDK](https://github.com/Azure/azure-functions-python-worker/issues/507). When using bindings, the constraint is that filenames that are used to store outputs are not customisable, they are limited to the ID `{rand-guid}`. The previous link shows how to use the SDK to give more control over the names of the output files.

[Here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob) is a reference Blob Storage bindings 

You can not replace the boilerplate code in `__init__.py` with code that calls the common library code.

The final step is to install the `Azurite` VSCode Extension for local development. At this atage we will also need to install the Azure Storage Explorer. One variable (`AzureWebJobsStorage`) in `local.settings.json` needs to change in order to use the storage emulator. After the edit, the file will look as follows
```
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "FUNCTIONS_EXTENSION_VERSION": "~3",
    "APPINSIGHTS_INSTRUMENTATIONKEY": "XXXXX"
  }
}
```
**Note: Using Azurite in VSCode** Despite the fact that I only use Blobs here (and not Queues), I need to start the Azurite Blob Service **and** the Azurite Queue Service. If I do not start the queue service, when I try to debug my function, it fails with an error similar to `"microsoft.windowsazure.storage: no connection could be made because the target machine actively refused it"`.

