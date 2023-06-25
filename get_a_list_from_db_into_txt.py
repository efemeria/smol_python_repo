#!/usr/bin/env python3
"""
Get a server list from a database, store it in a txt file
"""
import requests


def main():
  params = {
      'query': 'query_name{group="servers"}',
  }

  response = requests.get(
      'https://database.net:port/api/v1/query',
      params=params,
      auth=('username', 'password'),
  )

  server_list = response.json()

  db_servers = []
  for item in db_servers['data']['result']:
      all_servers.append(item['metric']['server'])

  return all_servers


if __name__ == "__main__":
    servers_list=main()
    with open('filename.txt', 'w') as f:
        print('\n'.join(map(str, servers_list)), file=f)
