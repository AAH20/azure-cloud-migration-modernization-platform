param location string
param tags object

resource hub 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'vnet-migrationforge-hub'
  location: location
  tags: tags
  properties: {
    addressSpace: {addressPrefixes: ['10.20.0.0/16']}
    subnets: [
      {name: 'shared-services', properties: {addressPrefix: '10.20.1.0/24'}}
      {name: 'private-endpoints', properties: {addressPrefix: '10.20.2.0/24'}}
    ]
  }
}

output hubNetworkName string = hub.name
