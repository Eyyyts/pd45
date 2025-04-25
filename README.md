# pd45


### flow
1. `plates_1.py` detects a license plate and face
2. calls Security API to check if face matches regitered driver
3. Security API checks firebase plate's registered driver
4. if mismatch, a security alert is created in Firebase

### setup
#### Security API Setup
```bash
# install this first for the api
pip install flask firebase-admin requests

# run the api server
python security_api.py

# run the plate detection
python plates_1.py

# for testing endpoints, run this
python test_security_api.py
```
#### endpoints
- **POST /check_plate**: send plate from db then cross match to Firebase
- **GET /vehicles**: list all registered vehicles
- **GET /alerts**: list all security alerts
- **POST /alerts/{id}/resolve**: mark an alert as resolved (additional if u want cleaner alerts)

#### laravel

since i don't hve access to the web app laravel, look at this sample integration:
```php
// if you prefer to access using mysql db's field of security match
public function getUnresolvedAlerts()
{
    $alerts = DB::table('plate_numbers')
        ->where('security_match', false)
        ->where('date_time_scanned', '>=', now()->subDays(1))
        ->orderBy('date_time_scanned', 'desc')
        ->get();
    
    return response()->json([
        'alerts' => $alerts,
        'unresolved_count' => $alerts->count()
    ]);
}
```
- that checks a `security_match` flag for every detected unauthorized access
```php
// if you prefer to access using the api directly
/**
  * displaying the security alerts using the api
  */
public function index()
{
    try {
        $response = Http::get('http://localhost:5000/alerts');
        
        if ($response->successful()) {
            $alerts = $response->json()['alerts'] ?? [];
            
            $unresolvedAlerts = collect($alerts)
                ->filter(function($alert) {
                    return !($alert['resolved'] ?? false);
                })
                ->values();
            
            return view('security.alerts', [
                'alerts' => $alerts,
                'unresolvedCount' => $unresolvedAlerts->count()
            ]);
        }
        
        return view('security.alerts', [
            'error' => 'Failed to fetch alerts from API'
        ]);
    } catch (\Exception $e) {
        return view('security.alerts', [
            'error' => 'Error connecting to security API: ' . $e->getMessage()
        ]);
    }
}

/**
  * marking alert as resolved
  */
public function resolveAlert($alertId)
{
    try {
        $response = Http::post("http://localhost:5000/alerts/{$alertId}/resolve");
        
        if ($response->successful()) {
            return redirect()->back()->with('success', 'Alert marked as resolved');
        }
        
        return redirect()->back()->with('error', 'Failed to resolve alert');
    } catch (\Exception $e) {
        return redirect()->back()->with('error', 'Error: ' . $e->getMessage());
    }
}
```

#### Notes

- this is just an example, make sure to integrate it with routes and controllers.
- implement this before the fetching of mysql db's, security checks comes first 