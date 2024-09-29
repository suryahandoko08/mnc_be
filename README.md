1. Soal File tahap 1 ada di folder test_1
2. Untuk Soal File tahap 2 
    - Python3
      masuk kedalam folder cashflow jalankan perintah : "pip3 install -r requirements.txt"
    - Orm Sql Alchemy
    - Database Postgre
    - Queue menggunakan Kafka
    - running kafka dan database
      masuk kedalam folder cashflow lalu jalankan perintah : "docker-compose up -d"
      setup database , username dan password db ada di file config.py sama dengan yang ada di file docker-compose.yaml
    - running migration / atau bisa jalankan file cashflow.sql
      masuk kedalam folder cashflow jalankan perintah: "flask db upgrade"
    - running unit test
      masuk ke dalam folder cashflow lalu jalankan perintah  : "python3 -m unittest test_app.py"
    - testing Api melalui Postman : https://api.postman.com/collections/4131954-1114c802-103e-4a81-848c-091cd60764a9?access_key=PMAT-01J8YD8H7CHPNNR39GNWQJN1Q8
      import file postman lalu coba beberapa Api nya
      untuk api transfer ada 2 , yaitu tranfer langsung dan transfer yang di proses lewat background
    - testing Kafka consume transfer Process
      python3 kafka_consumer.py
    - running api masuk kedalam folder cashflow lalu jalankan perintah : python3 app.py
    
       
