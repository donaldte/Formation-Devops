import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Récupérer tous les instantanés EBS appartenant au compte AWS en cours
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Récupérer toutes les instances EC2 actives (état 'running')
    instances_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    active_instance_ids = set()  # Ensemble pour stocker les ID des instances actives

    # Extraire les ID des instances EC2 en cours d'exécution
    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Parcourir chaque instantané et le supprimer s'il n'est pas attaché à un volume 
    # ou si le volume n'est pas attaché à une instance en cours d'exécution
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')  # Récupérer l'ID du volume associé à l'instantané

        if not volume_id:
            # Supprimer l'instantané s'il n'est pas associé à un volume
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Supprimé l'instantané EBS {snapshot_id} car il n'était pas associé à un volume.")
        else:
            # Vérifier si le volume associé existe toujours
            try:
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                
                # Si le volume existe mais n'est attaché à aucune instance en cours d'exécution, supprimer l'instantané
                if not volume_response['Volumes'][0]['Attachments']:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Supprimé l'instantané EBS {snapshot_id} car il provenait d'un volume non attaché à une instance active.")
            
            except ec2.exceptions.ClientError as e:
                # Si le volume associé à l'instantané n'existe plus (peut avoir été supprimé)
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Supprimé l'instantané EBS {snapshot_id} car le volume associé n'a pas été trouvé.")
