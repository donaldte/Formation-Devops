CI/CD : Continuous Integration / Continuous Delivery
EC2 : Elastic Compute Cloud
S3 : Simple Storage Service
aws codecommit (git) --> git
aws codebuild (build , test) --> artefact(S3(versioned))
aws codedeploy (deploy(agent)) --> Ec2, ECs, Lambda, EKS,
aws codepipeline(souce(push(main, master)), build, deploy)