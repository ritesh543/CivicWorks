# StudioNet deployments

All ten deployment transactions reached `FINALIZED` on StudioNet, chain ID 61999. The RPC returned successful constructor execution and the published source matched the SHA-256 digest of each file in this archive.

| Contract | Explorer address | Deployment receipt |
| --- | --- | --- |
| AccessPath | [0x166786a187Cd5cAc0A22940EfFa850caDA6341d8](https://explorer-studio.genlayer.com/address/0x166786a187Cd5cAc0A22940EfFa850caDA6341d8) | [View transaction](https://explorer-studio.genlayer.com/tx/0x88ee36639b09786d5660ab7fa78fcf331382284af21436bcd6f010615a1a3d6a) |
| WorksConflict | [0x17d89e5f7Ca26A297e5D9690f2E19d1546B1b3d6](https://explorer-studio.genlayer.com/address/0x17d89e5f7Ca26A297e5D9690f2E19d1546B1b3d6) | [View transaction](https://explorer-studio.genlayer.com/tx/0x57d926a3a4ed46d9f6450d27b11d72c6db5c2b61b2dcb52a772cc369082523d1) |
| RepairMerge | [0x2107403e86c8a9Ab81E8160cCcC56570596A5a33](https://explorer-studio.genlayer.com/address/0x2107403e86c8a9Ab81E8160cCcC56570596A5a33) | [View transaction](https://explorer-studio.genlayer.com/tx/0xa36b08e93a382a6ca8babbd1b61ee00e8dd0bc1e8ca82ff8e6b500057979c129) |
| NoticeClock | [0xe668ca5c1d0AFB8A631cE1B3a028146DA6A244a8](https://explorer-studio.genlayer.com/address/0xe668ca5c1d0AFB8A631cE1B3a028146DA6A244a8) | [View transaction](https://explorer-studio.genlayer.com/tx/0x7a837a9e0b061b4d8a0140f4bfe87fa2e7d2f9ffaf2bcb66f67f61a9cd1c2ebc) |
| OpenFieldMap | [0xC4B6381f9bB9A0a30Fd988Fe753f94cD70909570](https://explorer-studio.genlayer.com/address/0xC4B6381f9bB9A0a30Fd988Fe753f94cD70909570) | [View transaction](https://explorer-studio.genlayer.com/tx/0x05687d6a734e5d714e2f9b2ecb9a141e5d124035678a6393967238d21bf7f0c0) |
| HandoffCondition | [0xbF6eAdCBBEF8174184B7C792EAbD1EDA8663F7a8](https://explorer-studio.genlayer.com/address/0xbF6eAdCBBEF8174184B7C792EAbD1EDA8663F7a8) | [View transaction](https://explorer-studio.genlayer.com/tx/0xc59e181b08f30d5c58f58d7c5e1786cac4402c6690357bff98c2d679f2112a7f) |
| DonationAllocation | [0xD2C897DC06b167bc9725aB02373C48991D344273](https://explorer-studio.genlayer.com/address/0xD2C897DC06b167bc9725aB02373C48991D344273) | [View transaction](https://explorer-studio.genlayer.com/tx/0x409bcd2ad62166c88090b85b2611cca3aec043045f0a10479a948c4e610cbb79) |
| MinutesCommitment | [0xAbf23eD48C1914086C873239Ef1452254B70C01B](https://explorer-studio.genlayer.com/address/0xAbf23eD48C1914086C873239Ef1452254B70C01B) | [View transaction](https://explorer-studio.genlayer.com/tx/0x26d1bd866a2ff68d72d5c8801c91fed0e7e61bd331c9c46407074f953c7dae50) |
| MeterContinuity | [0x38d1E3960cA3488315f20B6226F74d2830031520](https://explorer-studio.genlayer.com/address/0x38d1E3960cA3488315f20B6226F74d2830031520) | [View transaction](https://explorer-studio.genlayer.com/tx/0x446ab8bdbb5add26a8b95e395282e0308a6cb428c0e568c12b61179bc8d1ccc8) |
| PublicFeedPulse | [0xEbFF2D9379E1F9c9E38a13e5dC071f0aa415400a](https://explorer-studio.genlayer.com/address/0xEbFF2D9379E1F9c9E38a13e5dC071f0aa415400a) | [View transaction](https://explorer-studio.genlayer.com/tx/0x16aa616cc760a3f562fad2ced1fd0bb6d6800fb01866e562f3b5a00a20d065de) |

Initial public reads returned zero for `count()` on each instance. NoticeClock also returned its configured threshold of 1,440 minutes. The addresses and receipts were verified on 21 November 2026.

Run `npm run verify:live` to repeat the read-only check. See [deployment_info.json](deployment_info.json) for the recorded SHA-256 digests, receipts, constructor arguments, and public deployer address.
