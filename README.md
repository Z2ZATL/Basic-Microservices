# ระบบ Microservices ด้วย Docker Compose

## รายละเอียดโปรแกรม

- มี API 2 ตัว (API1, API2) สร้างด้วยภาษา Python (Flask)
- API1 และ API2 ทำงานใน container แยกกัน
- API1 รับ request จากผู้ใช้ แล้วส่งต่อไปยัง API2 จากนั้นนำคำตอบกลับมาตอบผู้ใช้
- มีการ print logs ทั้งบน API1 และ API2
- endpoint ของแต่ละ API สามารถเป็นอะไรก็ได้ (ใช้ `/api/message` และ `/api/hello`)
- deploy ทุกอย่างด้วย `docker-compose.yml`

## วิธี Deploy และทดสอบ

1. **ติดตั้ง Docker และ Docker Compose**
2. **เปิดเทอร์มินัลที่โฟลเดอร์โปรเจค**
3. **รันคำสั่ง**

   ```bash
   docker-compose up -d
   ```

4. **ทดสอบ API**
   - ทดสอบ API1 (Gateway):
     - เปิดเบราว์เซอร์หรือใช้ curl ไปที่ [http://localhost:8080/api/message](http://localhost:8080/api/message)
   - ทดสอบ API2 โดยตรง:
     - เปิดเบราว์เซอร์หรือใช้ curl ไปที่ [http://localhost:8081/api/hello](http://localhost:8081/api/hello)

5. **ดู logs**

   ```bash
   docker-compose logs
   ```

6. **หยุดการทำงาน**

   ```bash
   docker-compose down
   ```