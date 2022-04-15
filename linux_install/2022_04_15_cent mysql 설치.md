## cent mysql 설치

1. mysql 홈페이지에서 커뮤니티 버전 설치 페이지로 들어간 후 노떙큐 어쩌구 다운로드의 주소를 복사한다

2. terminal에서 sudo yum install -y 복사한주소    를 입력한다

3. 레포지토리 설치가 완료 되었다.

4. yum install -y mysql-server 를 통해 설치를 시작해준다

5. 설치가 완료되면 terminal에 *systemctl enable mysqld && systemctl start mysqld && systemctl status mysqld* 를 입력해서 서버를 시작해본다

6. *grep 'temporary password' /var/log/mysqld.log* 명령어를 사용해서 임시 비밀번호를 확인한다

7. 접속하고나면 비번을 한번 바꿔주기 전까지 뭔가 할 수 있는게 없다

8. ```sql
   mysql> alter user 'root'@'localhost' identified by 'MySQL2020!';
   ```

   입력해서 비번을 바꿔준다

9. ```sql
   mysql> CREATE USER 'root'@'%' IDENTIFIED BY 'P@ssW0rd';
   mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
   mysql> commit;
   mysql> flush privileges;
   ```

   유저를 새로 만들어서 모든 ip에서 접근을 허용할 수 있다.





<hr/>

비밀번호 변경할 때 정책으로 인해 원하는 형태로 바꾸지 못할 때가 있다. 그럴떄는 

```sql
SHOW VARIABLES LIKE 'validate_password%' #권한 수준을 확인한 후
SET GLOBAL validate_password_policy=LOW; #high,medium,low 중 하나로 변경해준다.
SET GLOBAL validate_password_length = <원하는 길이>; #원하는 길이를 설정하 수 있다.
select password('<테스트할 패스워드>'); #설정하기 전 오류가 발생하지 않는지 테스트해볼 수 있다.
```

