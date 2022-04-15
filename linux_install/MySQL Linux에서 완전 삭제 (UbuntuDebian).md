MySQL Linux에서 완전 삭제 (Ubuntu/Debian)

1. 시스템에 남아있는 MySQL 쓰레기가 없는지 확인

   ```bash
   sudo apt-get remove --purge mysql*
   ```

2. 모든 것이 깨끗한지 확인

   ```bash
   dpkg -l | grep mysql
   ```

3. 아직 쓰레기가 남아있다면 개별적으로 제거

   ```bash
   sudo apt-get remove --purge {쓰레기}
   
   # 예시
   # sudo apt-get remove --purge mysql-apt-config
   ```

4. 다른 모든 것들 청소

   ```bash
   sudo rm -rf /etc/mysql /var/lib/mysql
   sudo apt-get autoremove
   sudo apt-get autoclean
   ```

