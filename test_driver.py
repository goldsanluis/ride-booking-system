from models.driver import Driver

# Test if driver_id parameter works
try:
    d = Driver("Test", "ABC123", 4.5, driver_id="test123")
    print("✅ SUCCESS! Driver created with driver_id")
    print(f"   driver_id: {d.driver_id}")
except TypeError as e:
    print(f"❌ ERROR: {e}")
