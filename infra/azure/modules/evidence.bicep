param location string
param suffix string
param tags object

resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'migrationforge-law-${suffix}'
  location: location
  tags: tags
  properties: {
    retentionInDays: 30
    sku: {name: 'PerGB2018'}
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'migration${suffix}'
  location: location
  tags: tags
  sku: {name: 'Standard_LRS'}
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource receipts 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${storage.name}/default/migration-receipts'
  properties: {publicAccess: 'None'}
}

output workspaceName string = logs.name
