# Branches

## Main:

### master
origin/master is the main branch where the source code of HEAD [i.e. branch's latest commit] always reflects a production-ready state.

Rule of thumb:
- no direct commits, a pull request will be required for any changes
- branches allowed to merge into master: hotfix/\*, release/\*

***
### develop:
origin/develop is the main branch where the source code of HEAD always reflects a state with the latest delivered development changes for the next release.

**Example:** Feature A is slated for the next release and Feature B is not. Feature B can not be merged into develop until Feature A has merged into develop and a release branch is created.

***
## Supporting:

### release:
* branch from: develop
* merge into: master
* naming convention: release/version [e.g. release/1.0.0]

> note: minor bug fixes or comestics alterations are allowed on the branch. Major ones will require a new hotfix branch to be created.
```csharp
'create new branch from develop head'
//current version is 1.0.0
//if minor change -> 1.1.0
//if major change -> 2.0.0
Branch:
	parent: develop
	name: release/1.1.0
Commit:
	Branch: release/1.1.0
	message: 'Start v1.1.0-rc Release Candidate builds'
	tag: 1.1.0-rc1

//rc builds pass testing and QA
'start pull request to merge into master'
Pull Request:
	source branch: feature/my-new-feature
	target branch: master
	tag: 1.1.0
	message: 'Release into production v1.1.0'

Pull request approved => delete feature/my-new-feature
```
***
### feature:
* branch from: develop
* merge into: develop
* naming convention: [e.g. feature/my-new-feature]

> note: A feature branch not targetted for the release-to-be-built must wait until after the release branch is branched off before it can be merged into develop.

```csharp
'create new branch from develop head'
Branch:
	parent: develop
	name: feature/my-new-feature
	message: 'Starting development of my-new-feature'

//feature is ready for next release
'start pull request to merge into develop'
Pull Request:
	source branch: feature/my-new-feature
	target branch: master
	tag: 1.0.1
	message: 'Merging new feature for next release'

Pull request approved -> delete feature/my-new-feature
```

***

### hotfix:
* branch from: master
* merge into: master, develop
* naming convention: hotfix/kebab-case [e.g. hotfix/breaking-bug]
> note: this branch needs to be merged into both master and develop. two pull-requests are required. first, update master and tag the release then merge into develop.  
  
```csharp   
'start pull request to merge into master'
//current version is 1.0.0, a hot fix increases it by 0.0.1'
Pull Request:
	source branch: hotfix/breaking-bug
	target branch: master
	tag: 1.0.1
	message: 'Fix for production bug'

'pull request is approved and merged into master'
//now do a pull request to merge into develop
Pull Request:
	source branch: hotfix/breaking-bug
	target branch: develop
	tag: 1.0.1
	message: 'Fix for production bug'

Both pull requests approved -> delete hotfix/breaking-bug
```