from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://api.thegraph.com/subgraphs/name/balancer-labs/balancer")

def get_token_info(token):
  query = """
    query getPrice($symbol: String) {
      tokenPrices(where: {symbol: $symbol}) {
        name
        price
        poolLiquidity
      }
    }
  """
  data = client.execute(query=query, variables={"symbol":token})
  return data['data']['tokenPrices']
