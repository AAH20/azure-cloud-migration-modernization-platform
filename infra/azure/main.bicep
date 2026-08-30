targetScope = 'subscription'

param location string = deployment().location
param suffix string = uniqueString(subscription().id)

var tags = {
  project: 'Azure Cloud Migration Modernization Platform'
  product: 'MigrationForge'
  purpose: 'migration-assessment-evidence'
  website: 'a2zsoc.com'
}

resource evidenceRg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-migrationforge-evidence-${suffix}'
  location: location
  tags: tags
}

resource networkRg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-migrationforge-connectivity-${suffix}'
  location: location
  tags: tags
}

module evidence 'modules/evidence.bicep' = {
  name: 'migrationforge-evidence'
  scope: evidenceRg
  params: {
    location: location
    suffix: suffix
    tags: tags
  }
}

module network 'modules/network.bicep' = {
  name: 'migrationforge-connectivity'
  scope: networkRg
  params: {
    location: location
    tags: tags
  }
}

output evidenceResourceGroup string = evidenceRg.name
output connectivityResourceGroup string = networkRg.name
output workspaceName string = evidence.outputs.workspaceName
output hubNetworkName string = network.outputs.hubNetworkName
