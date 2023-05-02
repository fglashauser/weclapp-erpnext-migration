import config
import paramiko

class ERPNextBackup:
    def backup(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        key = paramiko.RSAKey.from_private_key_file(config.PVE_KEY_PATH)
        ssh.connect(config.PVE_HOST, username=config.PVE_USER, pkey=key)

        command = f'pct exec {config.EN_LXC_ID} -- docker exec {config.EN_DOCKER_CONTAINER_NAME} bench backup'
        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        ssh.close()

        if error:
            print(f"Error: {error}")
        else:
            print(f"Output: {output}")

    def restore(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        key = paramiko.RSAKey.from_private_key_file(config.PVE_KEY_PATH)
        ssh.connect(config.PVE_HOST, username=config.PVE_USER, pkey=key)

        # Liste der verfügbaren Backups abrufen
        command = f'pct exec {config.EN_LXC_ID} -- docker exec {config.EN_DOCKER_CONTAINER_NAME} bash -c "ls -1t {config.EN_BACKUP_PATH}*.sql.gz | head -n1"'
        stdin, stdout, stderr = ssh.exec_command(command)

        backups = stdout.readlines()
        error = stderr.read().decode('utf-8')

        if not backups:
            print("Keine Backups gefunden")
            return

        # Letztes verfügbares Backup auswählen
        latest_backup = backups[-1].strip()

        # Backup wiederherstellen
        command = f'pct exec {config.EN_LXC_ID} -- docker exec {config.EN_DOCKER_CONTAINER_NAME} bash -c "bench restore --mariadb-root-password {config.EN_MARIADB_ROOT_PASSWORD} {latest_backup}"'
        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        ssh.close()

        if error:
            print(f"Error: {error}")
        else:
            print(f"Output: {output}")
