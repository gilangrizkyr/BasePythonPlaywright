# 🎯 PENJELASAN LENGKAP: APA FRAMEWORK INI & GIMANA CARA PAKAINYA

## 🤔 FRAMEWORK INI UNTUK APA?

Framework ini adalah **AUTOMATED TESTING TOOL** untuk menjalankan test website/aplikasi **OTOMATIS** tanpa perlu click-click manual.

### Contoh Penggunaan:
- ✅ Testing login (username, password, error handling)
- ✅ Testing e-commerce (add to cart, checkout, payment)
- ✅ Testing form (validation, submit, response)
- ✅ Testing API endpoint (GET, POST, PUT, DELETE)
- ✅ Testing database (query, insert, update, delete)

---

## 📌 ANALOGI SEDERHANA

### ❌ TANPA Framework (Manual Testing):
```
1. Buka browser
2. Ketik username
3. Ketik password
4. Click login
5. Tunggu hasil
6. Cek apakah login berhasil
7. Tulis di Excel: PASS/FAIL
⏱️  Waktu: 5 menit per test
```

### ✅ DENGAN Framework (Automated Testing):
```
1. Tulis test code (sekali saja)
2. Jalankan: pytest tests/ -v
3. Framework otomatis jalankan 100 tests dalam 2 menit
4. Hasil report otomatis HTML (screenshot, error logs, dll)
⏱️  Waktu: 2 menit untuk 100 tests!
```

---

## 💡 CONTOH PRAKTIS #1: LOGIN TESTING

Kita akan membuat test untuk login website Google.

### File: `tests/test_login_google.py`

```python
import pytest
from core.config import config

class TestGoogleLogin:
    
    @pytest.mark.asyncio
    async def test_valid_login(self, page):
        """Test login dengan email dan password valid"""
        
        # 1. Buka website
        await page.goto("https://accounts.google.com/login")
        
        # 2. Isi email
        await page.fill("input[type='email']", "user@gmail.com")
        await page.click("button:has-text('Next')")
        
        # 3. Tunggu halaman password
        await page.wait_for_selector("input[type='password']")
        
        # 4. Isi password
        await page.fill("input[type='password']", "password123")
        await page.click("button:has-text('Next')")
        
        # 5. Tunggu dashboard load
        await page.wait_for_url("**/myaccount.google.com/**")
        
        # 6. Verifikasi sudah login (lihat profile name)
        profile = await page.get_text(".profile-name")
        assert profile == "John Doe"
        
        print("✅ Test login BERHASIL!")
    
    
    @pytest.mark.asyncio
    async def test_invalid_password(self, page):
        """Test login dengan password salah"""
        
        await page.goto("https://accounts.google.com/login")
        await page.fill("input[type='email']", "user@gmail.com")
        await page.click("button:has-text('Next')")
        
        await page.wait_for_selector("input[type='password']")
        await page.fill("input[type='password']", "wrongpassword")
        await page.click("button:has-text('Next')")
        
        # Verifikasi error message muncul
        error = await page.get_text(".error-message")
        assert "password" in error.lower()
        
        print("✅ Test error handling BERHASIL!")
```

### Cara Jalankan:
```bash
pytest tests/test_login_google.py -v
```

### Output:
```
test_login_google.py::TestGoogleLogin::test_valid_login PASSED
test_login_google.py::TestGoogleLogin::test_invalid_password PASSED

======================== 2 passed in 5.23s ========================
```

---

## 💡 CONTOH PRAKTIS #2: E-COMMERCE TESTING

Test untuk add to cart dan checkout.

### File: `tests/test_ecommerce.py`

```python
import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

class TestEcommerce:
    
    @pytest.mark.asyncio
    async def test_add_to_cart_and_checkout(self, page):
        """Test menambah product ke cart dan checkout"""
        
        # 1. Login dulu
        login_page = LoginPage(page)
        await login_page.login("user@example.com", "password123")
        
        # 2. Lihat daftar product
        product_page = ProductPage(page)
        await product_page.goto("https://shop.example.com/products")
        
        # 3. Click product pertama
        await product_page.click_product("Laptop Gaming")
        
        # 4. Add to cart
        await product_page.add_to_cart()
        
        # 5. Verifikasi toast "Added to cart" muncul
        await page.wait_for_selector(".toast:has-text('Added to cart')")
        
        # 6. Go to cart
        await product_page.goto_cart()
        
        # 7. Checkout
        cart_page = CartPage(page)
        await cart_page.proceed_to_checkout()
        await cart_page.fill_shipping_info()
        await cart_page.fill_payment_info()
        
        # 8. Submit order
        await cart_page.place_order()
        
        # 9. Verifikasi order berhasil
        await page.wait_for_url("**/order-success/**")
        order_number = await page.get_text(".order-number")
        assert order_number.startswith("ORD-")
        
        print(f"✅ Order berhasil dibuat: {order_number}")
```

---

## 💡 CONTOH PRAKTIS #3: API TESTING

Test untuk API endpoint.

### File: `tests/test_api.py`

```python
import pytest
from core.utils import APIUtilities

class TestAPI:
    
    @pytest.mark.asyncio
    async def test_get_users(self):
        """Test GET /api/users endpoint"""
        
        api = APIUtilities("https://api.example.com")
        
        # Kirim GET request
        response = await api.get("/users")
        
        # Verifikasi response
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert "name" in data[0]
        
        print("✅ API test BERHASIL!")
    
    
    @pytest.mark.asyncio
    async def test_create_user(self):
        """Test POST /api/users endpoint"""
        
        api = APIUtilities("https://api.example.com")
        
        # Data yang akan dikirim
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 25
        }
        
        # Kirim POST request
        response = await api.post("/users", json=payload)
        
        # Verifikasi response
        assert response.status_code == 201
        data = response.json()
        assert data["id"] > 0
        assert data["name"] == "John Doe"
        
        print(f"✅ User berhasil dibuat dengan ID: {data['id']}")
```

---

## 💡 CONTOH PRAKTIS #4: DATABASE TESTING

Test untuk verify data di database.

### File: `tests/test_database.py`

```python
import pytest
from core.utils import DatabaseUtilities

class TestDatabase:
    
    @pytest.mark.asyncio
    async def test_user_data_in_db(self):
        """Test verifikasi data user di database"""
        
        db = DatabaseUtilities(
            host="localhost",
            database="app_db",
            user="root",
            password="password"
        )
        
        # Query: Get user by email
        query = "SELECT * FROM users WHERE email = %s"
        user = await db.fetch_one(query, ("john@example.com",))
        
        # Verifikasi data
        assert user is not None
        assert user['name'] == "John Doe"
        assert user['active'] == True
        
        print("✅ User data di database VALID!")
    
    
    @pytest.mark.asyncio
    async def test_insert_user(self):
        """Test insert user ke database"""
        
        db = DatabaseUtilities(
            host="localhost",
            database="app_db",
            user="root",
            password="password"
        )
        
        # Insert user
        query = """
            INSERT INTO users (name, email, age) 
            VALUES (%s, %s, %s)
        """
        await db.execute(query, ("Jane Doe", "jane@example.com", 28))
        
        # Verifikasi user tersimpan
        verify_query = "SELECT * FROM users WHERE email = %s"
        user = await db.fetch_one(verify_query, ("jane@example.com",))
        
        assert user is not None
        assert user['name'] == "Jane Doe"
        
        print("✅ User berhasil disimpan ke database!")
```

---

## 🔧 FITUR UTAMA FRAMEWORK

### 1. PAGE OBJECTS ✅
- Organize test code dengan baik
- Reusable code (DRY - Don't Repeat Yourself)
- Easy maintenance

**Contoh:**
```python
# pages/login_page.py
from core.base import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button:has-text('Login')"
    
    async def login(self, email, password):
        await self.fill(self.EMAIL_INPUT, email)
        await self.fill(self.PASSWORD_INPUT, password)
        await self.click(self.LOGIN_BUTTON)
        await self.wait_for_navigation()

# tests/test_login.py
async def test_login(self, page):
    login = LoginPage(page)
    await login.login("user@example.com", "password123")
```

### 2. DECORATORS ✅
- **@screenshot_on_failure** - Ambil screenshot saat test gagal
- **@retry_on_failure** - Retry test yang fail otomatis
- **@performance_monitor** - Ukur performa page load
- **@step** - Log setiap step dalam test

**Contoh:**
```python
from decorators import screenshot_on_failure, retry_on_failure

@screenshot_on_failure
@retry_on_failure(retries=3)
async def test_login(self, page):
    await page.goto("https://example.com")
    # ... test code ...
```

### 3. FIXTURES ✅
Ready-to-use fixtures:
- **page** - Browser page object (untuk web testing)
- **browser_context** - Browser context
- **api_client** - HTTP client (untuk API testing)
- **db_connection** - Database connection (untuk DB testing)

**Contoh:**
```python
async def test_login(self, page):  # Fixture page otomatis inject
    await page.goto("https://example.com")
    # ... test code ...

async def test_api(self, api_client):  # Fixture api_client otomatis inject
    response = await api_client.get("/users")
    # ... test code ...
```

### 4. UTILITIES ✅
Helper functions untuk berbagai kebutuhan:
- **DataGenerator** - Generate fake data (nama, email, dll)
- **FileManager** - Manage files & folders
- **WebUtilities** - Web helper functions
- **APIUtilities** - API helper functions
- **DatabaseUtilities** - Database helper functions
- **PerformanceUtilities** - Performance monitoring
- **SecurityUtilities** - Security testing

**Contoh:**
```python
from core.utils import DataGenerator

class TestSignup:
    async def test_signup(self, page):
        # Generate random email
        email = DataGenerator.email()
        name = DataGenerator.name()
        
        await page.fill("#email", email)
        await page.fill("#name", name)
        # ... continue test ...
```

### 5. REPORTERS ✅
Otomatis generate reports:
- HTML Report dengan screenshot
- JSON Report untuk CI/CD
- Allure Report (paling bagus)
- Screenshots on failure
- Browser logs & network logs

---

## 🎯 WORKFLOW TESTING YANG BENAR

Setiap test harus mengikuti pola: ARRANGE → ACT → ASSERT

```python
async def test_login(self, page):
    # ===== ARRANGE (Setup) =====
    await page.goto(config.base_url)  # Buka website
    # Prepare test data jika perlu
    
    # ===== ACT (Action) =====
    await page.fill("#email", "user@example.com")
    await page.fill("#password", "password123")
    await page.click("#login-button")
    
    # ===== ASSERT (Verify) =====
    await page.wait_for_url("**/dashboard/**")
    assert page.url.endswith("/dashboard")
    print("✅ Login test PASSED!")
```

---

## 📊 MARKERS (Kategorisasi Test)

Framework sudah setup markers untuk organize tests:

```bash
# Run hanya smoke tests (test cepat, basic functionality)
pytest -m smoke

# Run regression tests (comprehensive, semua features)
pytest -m regression

# Skip slow tests
pytest -m "not slow"

# Run hanya critical tests
pytest -m critical
```

Gunakan di test:
```python
@pytest.mark.smoke
async def test_login(self, page):
    # Test cepat
    pass

@pytest.mark.regression
async def test_complete_flow(self, page):
    # Test lengkap
    pass

@pytest.mark.slow
async def test_performance(self, page):
    # Test performa (butuh waktu lama)
    pass
```

---

## 🚀 PARALLEL EXECUTION (JAUH LEBIH CEPAT!)

Framework bisa jalankan multiple tests simultaneously:

```bash
# Jalankan parallel dengan 4 workers
pytest tests/ -n 4

# Atau auto (sesuai jumlah CPU core)
pytest tests/ -n auto
```

### Efek:
- 100 tests yang butuh 10 menit → jadi 2-3 menit saja!
- Hemat waktu CI/CD pipeline
- Faster feedback time untuk developers

---

## 📈 GENERATE REPORTS

```bash
# HTML Report (paling mudah dibaca)
pytest tests/ --html=reports/report.html
# Kemudian buka: open reports/report.html

# JSON Report (untuk CI/CD integration)
pytest tests/ --json=reports/report.json

# Allure Report (paling profesional)
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Report Include:
- ✅ Test results (PASS/FAIL)
- ✅ Execution time untuk setiap test
- ✅ Screenshots saat test gagal
- ✅ Error messages & stack traces
- ✅ Browser logs & network logs
- ✅ Video recording (optional)

---

## 💼 GUNANYA DI MANA?

Framework ini digunakan untuk:

1. **Development** - Test sebelum launch feature baru
2. **Regression Testing** - Memastikan fix bug tidak buat bug baru
3. **Continuous Integration** - Auto test setiap ada commit
4. **Production Monitoring** - Monitor aplikasi uptime 24/7
5. **Performance Testing** - Ukur kecepatan loading & response time
6. **Security Testing** - Periksa vulnerability

---

## ✅ KAPAN GUNAKAN FRAMEWORK INI?

### ✅ GUNAKAN untuk:
- Website punya 10+ features
- Perlu test regression
- Frequent releases (daily/weekly)
- Need CI/CD automation
- Team testing (multiple testers)
- Long-term project (6 bulan+)

### ❌ TIDAK PERLU untuk:
- Simple website (1-2 fitur saja)
- One-time testing
- Manual testing sudah cukup
- Tidak ada CI/CD pipeline

---

## 🎓 KESIMPULAN

Framework ini adalah **AUTOMATION TESTING TOOL** untuk:
- ✅ Menjalankan test OTOMATIS (bukan manual)
- ✅ Menghemat WAKTU (100x lebih cepat)
- ✅ Mengurangi HUMAN ERROR
- ✅ Membuat CONSISTENT RESULTS
- ✅ Dokumentasi OTOMATIS (report HTML)
- ✅ CI/CD READY (integrate dengan GitHub/GitLab)

---

## 🚀 LANGKAH BERIKUTNYA

1. **Baca dokumentasi:**
   - [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command quicksheet
   - [USAGE_GUIDE.md](USAGE_GUIDE.md) - Panduan lengkap

2. **Jalankan contoh test:**
   ```bash
   pytest tests/test_example.py -v
   ```

3. **Buat test pertama Anda:**
   - Copy template dari QUICK_REFERENCE.md
   - Buat file `tests/test_my_first_test.py`
   - Jalankan: `pytest tests/test_my_first_test.py -v`

4. **Lihat report:**
   ```bash
   open reports/report.html
   ```

---

**Selamat! Sekarang Anda understand framework ini. Mulai buat test sendiri sekarang! 🚀**
