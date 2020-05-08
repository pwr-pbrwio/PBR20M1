# UnleashedSZZ

## 0
```
	{
		"bugFixingId": "a6e8a13a2da6df08f4426cc4f623ec5c76078ba9",
		"bugInducingId": "ffce83512370e970426f7f6b7cff8f519de59bd4"
	},
    {
		"bugFixingId": "472048297814559b81251dcca98ee662ea09f14d",
		"bugInducingId": "c6639c9842973a7954c8baa412d6825cb833d51f"
	},
    { // Matching based on changelog file
		"bugFixingId": "4b16ebc144b164434f4aca40f103c216e6a4ced3",
		"bugInducingId": "23d4f2b1a237a3bcdcfe8f316c26a55c1d71ca6b"
	},
    {
		"bugFixingId": "217107e26bef95aeb8f669013e03191406b9c7ee",
		"bugInducingId": "2789d1df02e697ea511867546dc569ff6b405ece"
	},
    {
		"bugFixingId": "05287a9c14db8d145f61ea09ec2c61f4f0221cc6",
		"bugInducingId": "d5036dad6041cc0d12d3e2d1d1c49a29c4f731e0"
	},
	{ // Match based on changelog. Commits span over 7 years
		"bugFixingId": "6b85723d2db06b94af82b9e10d4c742838b2222e",
		"bugInducingId": "cef5978969bedfe066f903834a9ea4af6d508844"
	},
```

## 0.5
```
	{ // Inducing commit adds the whole c library
		"bugFixingId": "7f9dd70384c16e81a08fb8055ffa194bf72bdd7d",
		"bugInducingId": "7beb7dad9505746944744c20dbabca0b46d76585"
	},
    { // a lot of refactoring work along with logic changes in inducing commit. Hard to estimate the impact.
		"bugFixingId": "c5d28b03b72253f2ca6d9142a17487b253317ec6",
		"bugInducingId": "da1e988798fd0336a893e16e94d699e6b156c941"
	},
	{ // Most likely not a valid match. Huge single file refactoring in inducing commit (rather moving logic then changing it).
		"bugFixingId": "e129e7a0b64d6555460d240be2d79e53aaa1bef9",
		"bugInducingId": "b67088488ed98f2d21dc374a5a67be622cd8e046"
	},
```

## 1
```
	{
		"bugFixingId": "c1eab643af684a89b2ce957f60913c7710f7cf8e",
		"bugInducingId": "b21c2e528df0938471f7f1897964903fe1fc0a42"
	},
```

# OpenSZZ

Commit e043c322f12d56da0fc88131628edf0731c0f8e4 induces 79 fixes.

## 1
```
	{
		"bugFixingId": "b8c8937029ca7e15116e91c6a6c436368ac0f9bb",
		"bugFixingTs": "2018-12-20T15:07:14.000+0100",
		"bugFixingfileChanged": "zookeeper-server/src/test/java/org/apache/zookeeper/common/FileChangeWatcherTest.java",
		"bugInducingId": "e043c322f12d56da0fc88131628edf0731c0f8e4",
		"bugInducingTs": "2018-12-15T07:34:54.000+0100",
		"issueType": "Improvement"
	}
```

## 0
```
	{
		"bugFixingId": "6c7a273bc1c553be34dc7b9e658c6c16b8a023ef",
		"bugFixingTs": "2020-03-26T22:12:18.000+0100",
		"bugFixingfileChanged": "zookeeper-server/src/main/java/org/apache/zookeeper/server/FinalRequestProcessor.java",
		"bugInducingId": "11c07921c15e2fb7692375327b53f26a583b77ca",
		"bugInducingTs": "2019-10-10T14:37:45.000+0200",
		"issueType": "Improvement"
	},
	{
		"bugFixingId": "d784e4dc8e042bd622500f861163bb315fa856fe",
		"bugFixingTs": "2019-12-28T16:17:54.000+0100",
		"bugFixingfileChanged": "zookeeper-server/src/test/java/org/apache/zookeeper/test/ObserverMasterTest.java",
		"bugInducingId": "e043c322f12d56da0fc88131628edf0731c0f8e4",
		"bugInducingTs": "2018-12-15T07:34:54.000+0100",
		"issueType": "Improvement"
	},
	{ // Inducing commit is a huge refactoring commit
		"bugFixingId": "ae68c7d50e4057ef3f9b99ac0cd0200a8bd5f235",
		"bugFixingTs": "2019-11-21T05:58:30.000+0100",
		"bugFixingfileChanged": "zookeeper-server/src/main/java/org/apache/zookeeper/server/NettyServerCnxn.java",
		"bugInducingId": "fe940cdd8fb23ba09684cefb73233d570f4a20fa",
		"bugInducingTs": "2019-08-17T17:13:15.000+0200",
		"issueType": "Improvement"
	},
	{
		"bugFixingId": "a89c0942e45bb16e5282eee9d3a56ebbddbaae15",
		"bugFixingTs": "2019-07-31T11:02:00.000+0200",
		"bugFixingfileChanged": "zookeeper-server/src/main/java/org/apache/zookeeper/server/quorum/QuorumCnxManager.java",
		"bugInducingId": "e043c322f12d56da0fc88131628edf0731c0f8e4",
		"bugInducingTs": "2018-12-15T07:34:54.000+0100",
		"issueType": "Bug"
	},
```