import asyncio
import os

from anchorpy import Provider
from anchorpy import Wallet
from driftpy.drift_client import AccountSubscriptionConfig
from driftpy.drift_client import DriftClient
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair


async def get_all_market_names():
    env = "mainnet-beta"  # 'devnet'
    rpc = os.environ.get("MAINNET_RPC_ENDPOINT")
    kp = Keypair()  # random wallet
    wallet = Wallet(kp)
    connection = AsyncClient(rpc)
    provider = Provider(connection, wallet)
    drift_client = DriftClient(
        provider.connection,
        provider.wallet,
        env.split("-")[0],
        account_subscription=AccountSubscriptionConfig("cached"),
    )

    all_perps_markets = await drift_client.program.account["PerpMarket"].all()
    sorted_all_perps_markets = sorted(
        all_perps_markets, key=lambda x: x.account.market_index
    )
    result_perp = [
        bytes(x.account.name).decode("utf-8").strip() for x in sorted_all_perps_markets
    ]
    print("Perp Markets:")
    for market in result_perp:
        print(market)

    all_spot_markets = await drift_client.program.account["SpotMarket"].all()
    sorted_all_spot_markets = sorted(
        all_spot_markets, key=lambda x: x.account.market_index
    )
    result_spot = [
        bytes(x.account.name).decode("utf-8").strip() for x in sorted_all_spot_markets
    ]
    print("\n\nSpot Markets:")
    for market in result_spot:
        print(market)

    result = result_perp + result_spot[1:]
    return result


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    answer = loop.run_until_complete(get_all_market_names())
    print(answer)
