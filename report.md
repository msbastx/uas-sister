# LAPORAN UAS SISTEM TERDISTRIBUSI

## Judul Proyek

**Implementasi Sistem Event Aggregation dengan Arsitektur Microservices menggunakan Docker, FastAPI, Redis, dan PostgreSQL**

---

## 1. Pendahuluan

Pada era sistem terdistribusi modern, arsitektur monolitik mulai ditinggalkan dan digantikan oleh arsitektur **microservices** yang lebih modular, scalable, dan mudah dipelihara. Setiap layanan memiliki tanggung jawab yang terisolasi dan dapat dikembangkan maupun dijalankan secara independen.

Proyek ini dibuat sebagai bagian dari **Ujian Akhir Semester (UAS) mata kuliah Sistem Terdistribusi**, dengan tujuan mengimplementasikan sistem pemrosesan event secara terdistribusi yang mendukung:

* Pengiriman event secara paralel
* Pemrosesan terdistribusi
* Mekanisme deduplikasi
* Pengumpulan statistik sistem

---

## 2. Tujuan Proyek

Tujuan utama dari proyek ini adalah:

1. Mengimplementasikan arsitektur microservices sederhana
2. Menerapkan komunikasi antar service melalui message queue
3. Menangani concurrency dan deduplikasi data
4. Menyediakan endpoint monitoring statistik sistem
5. Menggunakan Docker sebagai platform orkestrasi service

---

## 3. Arsitektur Sistem

Sistem ini terdiri dari beberapa komponen utama:

### 3.1 Publisher Service

* Bertugas menerima request dari client
* Menyediakan endpoint `/publish`
* Menerima sekumpulan event dalam bentuk JSON
* Meneruskan event ke message broker (Redis)

### 3.2 Broker (Redis)

* Digunakan sebagai message queue
* Menyimpan event secara sementara
* Menjadi media komunikasi antara Publisher dan Aggregator

### 3.3 Aggregator Service

* Mengambil event dari Redis
* Melakukan deduplikasi berdasarkan `event.id`
* Menyimpan event unik ke database
* Menghitung statistik sistem
* Menyediakan endpoint `/stats`

### 3.4 Storage (PostgreSQL)

* Menyimpan data event yang telah diproses
* Menyimpan data secara persisten

---

## 4. Struktur Proyek

Struktur direktori proyek adalah sebagai berikut:

```
UAS-SISTER
│
├── aggregator
│   ├── app
│   │   ├── consumer.py
│   │   ├── db.py
│   │   ├── init.sql
│   │   ├── main.py
│   │   ├── models.py
│   │   └── redis_queue.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── publisher
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── tests
│   ├── test_concurrency.py
│   ├── test_dedup.py
│   └── test_stats.py
│
├── docker-compose.yml
└── README.md
```

---

## 5. Teknologi yang Digunakan

| Teknologi      | Fungsi                   |
| -------------- | ------------------------ |
| Python         | Bahasa pemrograman utama |
| FastAPI        | Framework web service    |
| Redis          | Message broker / queue   |
| PostgreSQL     | Database penyimpanan     |
| Docker         | Containerization         |
| Docker Compose | Orkestrasi service       |

---

## 6. Alur Kerja Sistem

1. Client mengirim request ke endpoint `/publish`
2. Publisher menerima event dan mendorongnya ke Redis
3. Aggregator mengambil event dari Redis
4. Event diproses dan dilakukan deduplikasi
5. Event unik disimpan ke PostgreSQL
6. Statistik sistem diperbarui
7. Client dapat mengakses `/stats` untuk melihat status sistem

---

## 7. Endpoint API

### 7.1 POST /publish

Digunakan untuk mengirimkan event

**Contoh Request:**

```json
[
  {"id": "evt-1", "payload": {"value": 100}},
  {"id": "evt-2", "payload": {"value": 200}}
]
```

**Response:**

```json
{
  "status": "accepted",
  "count": 2
}
```

---

### 7.2 GET /stats

Menampilkan statistik sistem

**Response:**

```json
{
  "received": 10,
  "unique_processed": 8,
  "duplicate_dropped": 2
}
```

---

## 8. Pengujian Sistem

Pengujian dilakukan menggunakan beberapa skenario:

1. **Concurrency Test**

   * Mengirim banyak event secara paralel
   * Memastikan sistem tetap stabil

2. **Deduplication Test**

   * Mengirim event dengan ID yang sama
   * Memastikan hanya event unik yang disimpan

3. **Statistics Test**

   * Memverifikasi keakuratan data pada endpoint `/stats`

---

## 9. Hasil dan Pembahasan

Berdasarkan hasil pengujian:

* Sistem mampu menangani request secara paralel
* Event duplikat berhasil dideteksi dan dibuang
* Statistik sistem tercatat dengan benar
* Setiap service berjalan independen sesuai konsep microservices

Arsitektur ini membuktikan bahwa sistem terdistribusi dapat diimplementasikan secara sederhana namun efektif menggunakan teknologi modern.

---

## 10. Kesimpulan

Proyek ini berhasil mengimplementasikan sistem event aggregation berbasis microservices. Dengan memanfaatkan Docker, FastAPI, Redis, dan PostgreSQL, sistem dapat berjalan secara terisolasi, scalable, dan mudah dikembangkan.

Implementasi ini memenuhi konsep utama sistem terdistribusi, yaitu pemisahan tanggung jawab, komunikasi antar service, serta fault isolation.

---

## 11. Saran Pengembangan

Beberapa pengembangan lanjutan yang dapat dilakukan:

* Menambahkan autentikasi dan otorisasi
* Implementasi retry mechanism
* Monitoring dengan Prometheus & Grafana
* Scaling aggregator secara horizontal

---

## 12. Penutup

Demikian laporan UAS Sistem Terdistribusi ini dibuat sebagai dokumentasi dan bentuk pertanggungjawaban akademik atas proyek yang telah dikembangkan.

---

**Nama Mahasiswa**: Shadam Bastian
**Mata Kuliah**: Sistem Terdistribusi
**Tahun Akademik**: 2025
