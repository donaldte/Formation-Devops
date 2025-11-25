# branche 
 --> staging
 --> pre-prod
 --> post-merge
 --> release/xyz
 --> tags v1.0.0, v1.1.0 , v2.0.0
 --> hotfix/xyz

 git init 
 git add . 
 git commit -m "feat: initialisation application Flask avec route /hello"
      --feat 
      --fix 
      --test 
      --doc 
      --style 
      --refactor 
      --perf 
      --build 
      --ci 
      --chore 
      --revert 
      --release 
      --wip
 git checkout -b test/unit-tests
 git branch -d test/unit-tests
 git checkout -b test/unit-tests
 git merge --no-ff feature/add-hello-route
 git checkout main
 git merge test/unit-tests
 git branch -d test/unit-tests


# tags 
git tag -a v1.0.0 -m "Release stable v1.0.0"
git push origin v1.0.0