# ------------------------------------------------------------
# IFSC Code Finder API - Nexxon Hackers Edition
# Developed by: Creator Shyamchand & Ayan
# Organization: CEO & Founder Of - Nexxon Hackers
# Data Source: Razorpay IFSC API (Free & Open)
# ------------------------------------------------------------

from flask import Flask, request, jsonify, render_template_string
import requests
from collections import OrderedDict
import re
import json
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ---------------- CONFIG ----------------
COPYRIGHT_STRING = "Creator Shyamchand & Ayan - CEO & Founder Of - Nexxon Hackers"
RAZORPAY_IFSC_URL = "https://ifsc.razorpay.com"

DESIRED_ORDER = [
    "ifsc_code", "bank_name", "bank_code", "branch", "address",
    "city", "district", "state", "centre", "contact",
    "micr_code", "swift_code", "iso3166",
    "imps_available", "neft_available", "rtgs_available", "upi_available",
    "checked_at"
]

# ---------------- HTML TEMPLATE ----------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
<title>IFSC Code Finder API - Nexxon Hackers</title>
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-java.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-cpp.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-php.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
<script>tailwind.config={theme:{extend:{colors:{primary:'#6366f1',secondary:'#4f46e5',accent:'#818cf8'},borderRadius:{'none':'0px','sm':'4px',DEFAULT:'8px','md':'12px','lg':'16px','xl':'20px','2xl':'24px','3xl':'32px','full':'9999px','button':'8px'}}}}</script>
<style>
:root { --primary: #6366f1; --secondary: #4f46e5; }
.gradient-bg { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 50%, #3730a3 100%); }
.gradient-card { background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); }
.glass-effect { backdrop-filter: blur(10px); background: rgba(255,255,255,0.8); }
.endpoint-card { transition: all 0.3s ease; border-left: 4px solid var(--primary); }
.endpoint-card:hover { transform: translateX(4px); box-shadow: 0 20px 25px -5px rgba(99,102,241,0.2); }
.code-block { max-height: 400px; overflow-y: auto; }
pre { margin: 0 !important; border-radius: 8px !important; }
.tab-btn { transition: all 0.2s; cursor: pointer; }
.tab-btn.active { background: #6366f1 !important; color: white !important; box-shadow: 0 4px 6px -1px rgba(99,102,241,0.3); }
.pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.typing::after { content: '|'; animation: blink 1s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
.json-viewer { background: #1e1e1e; border-radius: 8px; padding: 16px; overflow-x: auto; font-family: 'Monaco','Menlo',monospace; font-size: 13px; max-height: 500px; }
.json-key { color: #9cdcfe; } .json-string { color: #ce9178; } .json-number { color: #b5cea8; }
.bank-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.hover-scale { transition: transform 0.2s; }
.hover-scale:hover { transform: scale(1.05); }
</style>
</head>
<body class="bg-gradient-to-br from-indigo-50 via-white to-purple-50 min-h-screen">
<main class="pt-4 md:pt-8 pb-8 md:pb-12 px-3 md:px-4 max-w-7xl mx-auto">
    
    <!-- Floating Header -->
    <header class="text-center py-6 md:py-10">
        <div class="relative inline-block">
            <div class="absolute inset-0 gradient-bg rounded-full blur-2xl opacity-30 pulse"></div>
            <div class="relative bank-icon w-16 h-16 md:w-24 md:h-24 gradient-bg rounded-2xl md:rounded-3xl mb-4 md:mb-6 shadow-xl mx-auto">
                <svg class="w-8 h-8 md:w-12 md:h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
            </div>
        </div>
        <h1 class="text-3xl md:text-5xl font-extrabold text-gray-900 mb-2">
            <span class="gradient-bg bg-clip-text text-transparent">IFSC Code Finder</span>
        </h1>
        <p class="text-base md:text-xl text-gray-600 mb-2">Instant Bank Branch Details from IFSC Code</p>
        <p class="text-xs md:text-md text-gray-500">🏦 150,000+ Branches • 200+ Banks • Real-time Data</p>
        <div class="mt-3 md:mt-4 inline-flex flex-wrap justify-center gap-1 md:gap-2">
            <span class="px-2 md:px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs md:text-sm font-medium"><i class="ri-check-line mr-1"></i>100% Free</span>
            <span class="px-2 md:px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs md:text-sm font-medium"><i class="ri-key-2-line mr-1"></i>No API Key</span>
            <span class="px-2 md:px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs md:text-sm font-medium"><i class="ri-database-2-line mr-1"></i>Real-time</span>
            <span class="px-2 md:px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-xs md:text-sm font-medium"><i class="ri-flashlight-line mr-1"></i>Fast Response</span>
        </div>
    </header>

    <!-- Live Test Section -->
    <section class="mb-8 md:mb-12 bg-white rounded-3xl p-4 md:p-8 shadow-xl border border-indigo-100 glass-effect">
        <div class="flex items-center gap-2 mb-4 md:mb-6">
            <div class="w-2 h-2 bg-green-500 rounded-full pulse"></div>
            <h2 class="text-lg md:text-2xl font-bold text-gray-900">🔍 Live API Test</h2>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-3 mb-4">
            <div class="flex-1 relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <i class="ri-bank-line text-gray-400"></i>
                </div>
                <input type="text" id="ifscInput" placeholder="Enter IFSC Code (e.g., SBIN0009174)" 
                       class="w-full pl-10 pr-4 py-3 md:py-4 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none text-sm md:text-base transition"
                       value="SBIN0009174"
                       oninput="this.value = this.value.toUpperCase()">
            </div>
            <button id="searchBtn" class="gradient-bg text-white px-6 md:px-8 py-3 md:py-4 rounded-xl font-semibold hover:shadow-xl transition hover-scale flex items-center justify-center gap-2 text-sm md:text-base">
                <i class="ri-search-line"></i>
                <span>Lookup IFSC</span>
            </button>
        </div>
        
        <!-- Quick Test Banks -->
        <div class="flex gap-2 mb-4 flex-wrap">
            <span class="text-xs text-gray-500 font-medium py-1"><i class="ri-flashlight-line"></i> Try:</span>
            <button onclick="document.getElementById('ifscInput').value='SBIN0009174'; document.getElementById('searchBtn').click()" 
                    class="text-xs bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-full text-indigo-700 transition border border-indigo-200 font-medium hover-scale">
                🏦 SBI
            </button>
            <button onclick="document.getElementById('ifscInput').value='HDFC0000123'; document.getElementById('searchBtn').click()" 
                    class="text-xs bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-full text-indigo-700 transition border border-indigo-200 font-medium hover-scale">
                🏦 HDFC
            </button>
            <button onclick="document.getElementById('ifscInput').value='ICIC0000001'; document.getElementById('searchBtn').click()" 
                    class="text-xs bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-full text-indigo-700 transition border border-indigo-200 font-medium hover-scale">
                🏦 ICICI
            </button>
            <button onclick="document.getElementById('ifscInput').value='YESB0DNB002'; document.getElementById('searchBtn').click()" 
                    class="text-xs bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-full text-indigo-700 transition border border-indigo-200 font-medium hover-scale">
                🏦 YES Bank
            </button>
        </div>
        
        <!-- Response Area -->
        <div id="responseContainer" class="hidden">
            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                    <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span class="text-sm font-semibold text-gray-700">API Response</span>
                    <span id="responseTime" class="text-xs text-gray-400"></span>
                </div>
                <button id="copyBtn" class="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-600 px-3 py-1.5 rounded-lg transition flex items-center gap-1 font-medium">
                    <i class="ri-file-copy-line"></i> Copy JSON
                </button>
            </div>
            <pre id="responseDisplay" class="json-viewer"></pre>
        </div>
        
        <!-- Loading -->
        <div id="loadingIndicator" class="hidden text-center py-8">
            <div class="inline-block w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
            <p class="mt-3 text-gray-500 font-medium typing">Fetching bank details...</p>
        </div>
        
        <!-- Error -->
        <div id="errorDisplay" class="hidden bg-red-50 border-2 border-red-200 rounded-xl p-4 text-red-700">
            <div class="flex items-center gap-2"><i class="ri-error-warning-line text-xl"></i><span class="font-semibold">Error</span></div>
            <p id="errorMessage" class="text-sm mt-1"></p>
        </div>
    </section>

    <!-- Stats Grid -->
    <section class="mb-8 md:mb-12 grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
        <div class="bg-white rounded-xl p-3 md:p-4 shadow-sm text-center border border-indigo-100">
            <i class="ri-bank-line text-indigo-500 text-2xl md:text-3xl"></i>
            <p class="text-lg md:text-2xl font-bold text-gray-900">150K+</p>
            <p class="text-xs text-gray-500">Branches</p>
        </div>
        <div class="bg-white rounded-xl p-3 md:p-4 shadow-sm text-center border border-indigo-100">
            <i class="ri-building-2-line text-indigo-500 text-2xl md:text-3xl"></i>
            <p class="text-lg md:text-2xl font-bold text-gray-900">200+</p>
            <p class="text-xs text-gray-500">Banks</p>
        </div>
        <div class="bg-white rounded-xl p-3 md:p-4 shadow-sm text-center border border-indigo-100">
            <i class="ri-checkbox-circle-line text-green-500 text-2xl md:text-3xl"></i>
            <p class="text-lg md:text-2xl font-bold text-gray-900">99.9%</p>
            <p class="text-xs text-gray-500">Uptime</p>
        </div>
        <div class="bg-white rounded-xl p-3 md:p-4 shadow-sm text-center border border-indigo-100">
            <i class="ri-timer-flash-line text-orange-500 text-2xl md:text-3xl"></i>
            <p class="text-lg md:text-2xl font-bold text-gray-900">&lt;500ms</p>
            <p class="text-xs text-gray-500">Response Time</p>
        </div>
    </section>

    <!-- API Documentation -->
    <section class="mb-8 md:mb-12">
        <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4 md:mb-6 text-center">
            <span class="gradient-bg bg-clip-text text-transparent">📡 API Documentation</span>
        </h2>
        
        <!-- Main Endpoint -->
        <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg mb-4 md:mb-6 endpoint-card">
            <div class="flex items-center justify-between mb-3 md:mb-4">
                <div class="flex items-center gap-2 md:gap-3">
                    <span class="w-10 h-10 gradient-bg rounded-xl flex items-center justify-center text-white text-lg">🔍</span>
                    <div>
                        <h3 class="text-lg md:text-xl font-bold text-gray-900">Lookup IFSC Code</h3>
                        <p class="text-xs md:text-sm text-gray-500">Get complete bank branch details from IFSC code</p>
                    </div>
                </div>
                <span class="px-3 py-1.5 bg-green-100 text-green-700 text-xs font-bold rounded-full">GET</span>
            </div>
            
            <div class="bg-gray-900 rounded-lg p-3 mb-3 overflow-x-auto">
                <code class="text-green-400 text-sm">/api/ifsc/{IFSC_CODE}</code>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                <div class="bg-gray-50 rounded-lg p-3">
                    <p class="text-xs font-semibold text-gray-700 mb-1">Path Parameter</p>
                    <code class="text-xs text-indigo-600">IFSC_CODE</code>
                    <p class="text-xs text-gray-500 mt-1">11-character alphanumeric code (e.g., SBIN0009174)</p>
                </div>
                <div class="bg-gray-50 rounded-lg p-3">
                    <p class="text-xs font-semibold text-gray-700 mb-1">Example</p>
                    <code class="text-xs text-indigo-600">/api/ifsc/SBIN0009174</code>
                </div>
            </div>
            
            <!-- Code Examples in 5 Languages -->
            <div class="mt-4 border-t pt-4">
                <p class="text-sm font-semibold mb-3">💻 Code Examples:</p>
                <div class="flex gap-1 md:gap-2 mb-3 flex-wrap">
                    <button onclick="showCode(this, 'code-python')" class="tab-btn active px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">🐍 Python</button>
                    <button onclick="showCode(this, 'code-java')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">☕ Java</button>
                    <button onclick="showCode(this, 'code-cpp')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">⚡ C++</button>
                    <button onclick="showCode(this, 'code-php')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">🐘 PHP</button>
                    <button onclick="showCode(this, 'code-js')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">📜 JavaScript</button>
                </div>
                
                <div id="code-python" class="code-block">
                    <pre class="language-python"><code>import requests

ifsc_code = "SBIN0009174"
url = f"https://api.example.com/api/ifsc/{ifsc_code}"

response = requests.get(url)
data = response.json()

if data.get("success"):
    print(f"🏦 Bank: {data['bank_name']}")
    print(f"📍 Branch: {data['branch']}")
    print(f"🏙️  City: {data['city']}")
    print(f"📞 Contact: {data['contact']}")
    print(f"💳 MICR: {data['micr_code']}")
    print(f"✅ UPI: {data['upi_available']}")
    print(f"✅ NEFT: {data['neft_available']}")
    print(f"✅ RTGS: {data['rtgs_available']}")
else:
    print(f"❌ Error: {data['error']}")</code></pre>
                </div>
                
                <div id="code-java" class="code-block hidden">
                    <pre class="language-java"><code>import java.net.http.*;
import java.net.URI;

public class IFSCLookup {
    public static void main(String[] args) throws Exception {
        String ifsc = "SBIN0009174";
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://api.example.com/api/ifsc/" + ifsc))
            .GET()
            .build();
        
        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenApply(HttpResponse::body)
            .thenAccept(System.out::println)
            .join();
    }
}</code></pre>
                </div>
                
                <div id="code-cpp" class="code-block hidden">
                    <pre class="language-cpp"><code>#include &lt;iostream&gt;
#include &lt;curl/curl.h&gt;
#include &lt;nlohmann/json.hpp&gt;

using json = nlohmann::json;

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* output) {
    output->append((char*)contents, size * nmemb);
    return size * nmemb;
}

int main() {
    std::string ifsc = "SBIN0009174";
    std::string url = "https://api.example.com/api/ifsc/" + ifsc;
    
    CURL* curl = curl_easy_init();
    std::string response;
    
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
        
        json data = json::parse(response);
        std::cout << "Bank: " << data["bank_name"] << std::endl;
        std::cout << "Branch: " << data["branch"] << std::endl;
    }
    return 0;
}</code></pre>
                </div>
                
                <div id="code-php" class="code-block hidden">
                    <pre class="language-php"><code>&lt;?php
$ifsc = "SBIN0009174";
$url = "https://api.example.com/api/ifsc/" . $ifsc;

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);

if ($data['success']) {
    echo "🏦 Bank: " . $data['bank_name'] . "\n";
    echo "📍 Branch: " . $data['branch'] . "\n";
    echo "🏙️  City: " . $data['city'] . "\n";
    echo "📞 Contact: " . $data['contact'] . "\n";
    echo "💳 MICR: " . $data['micr_code'] . "\n";
} else {
    echo "❌ Error: " . $data['error'] . "\n";
}
?&gt;</code></pre>
                </div>
                
                <div id="code-js" class="code-block hidden">
                    <pre class="language-javascript"><code>const ifsc = "SBIN0009174";
const url = `https://api.example.com/api/ifsc/${ifsc}`;

// Using fetch (Browser/Node.js 18+)
fetch(url)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(`🏦 Bank: ${data.bank_name}`);
            console.log(`📍 Branch: ${data.branch}`);
            console.log(`🏙️  City: ${data.city}`);
            console.log(`📞 Contact: ${data.contact}`);
            console.log(`💳 MICR: ${data.micr_code}`);
        } else {
            console.error(`❌ Error: ${data.error}`);
        }
    })
    .catch(err => console.error('Request failed:', err));

// Using async/await
async function lookupIFSC(ifsc) {
    try {
        const response = await fetch(
            `https://api.example.com/api/ifsc/${ifsc}`
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}</code></pre>
                </div>
            </div>
        </div>
        
        <!-- Response Fields -->
        <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg mb-4 md:mb-6">
            <h3 class="text-lg md:text-xl font-bold text-gray-900 mb-4">📋 Response Fields</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">bank_name</span><span class="text-sm text-gray-600">Full bank name</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">bank_code</span><span class="text-sm text-gray-600">Short bank code (4 chars)</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">branch</span><span class="text-sm text-gray-600">Branch name</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">city</span><span class="text-sm text-gray-600">City name</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">district</span><span class="text-sm text-gray-600">District name</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">state</span><span class="text-sm text-gray-600">State name</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">contact</span><span class="text-sm text-gray-600">Phone number</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">micr_code</span><span class="text-sm text-gray-600">MICR code (9 digits)</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">upi_available</span><span class="text-sm text-gray-600">UPI support (true/false)</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">neft_available</span><span class="text-sm text-gray-600">NEFT support (true/false)</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">rtgs_available</span><span class="text-sm text-gray-600">RTGS support (true/false)</span></div>
                <div class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded-lg"><span class="font-mono text-xs bg-gray-100 px-2 py-1 rounded">imps_available</span><span class="text-sm text-gray-600">IMPS support (true/false)</span></div>
            </div>
        </div>
        
        <!-- Sample Response -->
        <div class="bg-gray-900 rounded-2xl p-4 md:p-6">
            <h3 class="text-lg md:text-xl font-bold text-white mb-4 flex items-center gap-2">
                <i class="ri-code-box-line text-indigo-400"></i> Sample Response
            </h3>
            <pre class="text-green-400 text-xs overflow-x-auto">{
  "success": true,
  "ifsc_code": "SBIN0009174",
  "bank_name": "State Bank of India",
  "bank_code": "SBIN",
  "branch": "Delhi Nagrik Sehkari Bank IMPS",
  "address": "720, Near Ghantaghar, Subzi Mandi, Delhi - 110007",
  "city": "Mumbai",
  "district": "Delhi",
  "state": "Maharashtra",
  "centre": "Delhi",
  "contact": "+919560344685",
  "micr_code": "110196002",
  "swift_code": null,
  "iso3166": "IN-MH",
  "imps_available": true,
  "neft_available": true,
  "rtgs_available": true,
  "upi_available": true,
  "checked_at": "2026-04-24 10:30:45 UTC",
  "api_info": {
    "developed_by": "Creator Shyamchand & Ayan",
    "organization": "CEO & Founder Of - Nexxon Hackers"
  }
}</pre>
        </div>
    </section>

    <!-- Developer Credit -->
    <div class="text-center py-6 md:py-8">
        <div class="inline-block gradient-bg text-white px-6 md:px-10 py-4 md:py-5 rounded-2xl md:rounded-3xl shadow-xl">
            <p class="font-bold text-lg md:text-2xl">Developed by Creator Shyamchand & Ayan</p>
            <p class="text-sm md:text-lg opacity-95">CEO & Founder Of - Nexxon Hackers</p>
        </div>
        <p class="text-xs md:text-sm text-gray-500 mt-3">Data powered by Razorpay IFSC API • 100% Free & Open</p>
    </div>

</main>

<script>
function showCode(btn, id) {
    const parent = btn.parentElement.parentElement;
    parent.querySelectorAll('.code-block').forEach(b => b.classList.add('hidden'));
    parent.querySelectorAll('.tab-btn').forEach(b => {
        b.classList.remove('active', '!bg-indigo-600', 'text-white');
        b.classList.add('bg-gray-200');
    });
    document.getElementById(id).classList.remove('hidden');
    btn.classList.add('active', '!bg-indigo-600', 'text-white');
    btn.classList.remove('bg-gray-200');
}
document.querySelectorAll('.tab-btn.active').forEach(btn => {
    btn.classList.add('!bg-indigo-600', 'text-white');
    btn.classList.remove('bg-gray-200');
});

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\\s*:)?|\\b(true|false|null)\\b|-?\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d+)?)/g, function(m) {
        let cls = 'json-number';
        if (/^"/.test(m)) cls = m.includes(':') ? 'json-key' : 'json-string';
        else if (/true|false/.test(m)) cls = 'json-boolean';
        else if (/null/.test(m)) cls = 'json-null';
        return '<span class="' + cls + '">' + m + '</span>';
    });
}

async function fetchIFSC() {
    const ifsc = document.getElementById('ifscInput').value.trim().toUpperCase();
    if (!ifsc) { alert('Please enter an IFSC code'); return; }
    
    const responseContainer = document.getElementById('responseContainer');
    const responseTime = document.getElementById('responseTime');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorDisplay = document.getElementById('errorDisplay');
    
    responseContainer.classList.add('hidden');
    errorDisplay.classList.add('hidden');
    loadingIndicator.classList.remove('hidden');
    
    const startTime = Date.now();
    
    try {
        const response = await fetch('/api/ifsc/' + encodeURIComponent(ifsc));
        const data = await response.json();
        const elapsed = Date.now() - startTime;
        
        loadingIndicator.classList.add('hidden');
        responseTime.textContent = `(${elapsed}ms)`;
        
        const jsonStr = JSON.stringify(data, null, 2);
        document.getElementById('responseDisplay').innerHTML = syntaxHighlight(jsonStr);
        responseContainer.classList.remove('hidden');
        
    } catch (error) {
        loadingIndicator.classList.add('hidden');
        document.getElementById('errorMessage').textContent = error.message;
        errorDisplay.classList.remove('hidden');
    }
}

document.getElementById('searchBtn').addEventListener('click', fetchIFSC);
document.getElementById('ifscInput').addEventListener('keypress', (e) => { if (e.key === 'Enter') fetchIFSC(); });

document.getElementById('copyBtn').addEventListener('click', function() {
    const text = document.getElementById('responseDisplay').textContent;
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById('copyBtn');
        btn.innerHTML = '<i class="ri-check-line"></i> Copied!';
        setTimeout(() => btn.innerHTML = '<i class="ri-file-copy-line"></i> Copy JSON', 2000);
    });
});
</script>
</body>
</html>
'''

# ---------------- IFSC API LOGIC ----------------
def validate_ifsc_format(ifsc_code):
    """Validate IFSC code format"""
    pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
    return bool(re.match(pattern, ifsc_code.upper()))

def get_ifsc_details(ifsc_code):
    """Fetch IFSC details from Razorpay API"""
    ifsc_code = ifsc_code.upper().strip()
    
    # Validate format first
    if not validate_ifsc_format(ifsc_code):
        return {
            "success": False,
            "error": "Invalid IFSC format. Must be 11 characters: 4 letters + 0 + 6 alphanumeric (e.g., SBIN0009174)",
            "ifsc_code": ifsc_code
        }
    
    try:
        url = f"{RAZORPAY_IFSC_URL}/{ifsc_code}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Build clean response
            result = OrderedDict()
            result["success"] = True
            result["ifsc_code"] = data.get("IFSC", ifsc_code)
            result["bank_name"] = data.get("BANK", "N/A")
            result["bank_code"] = data.get("BANKCODE", "N/A")
            result["branch"] = data.get("BRANCH", "N/A")
            result["address"] = data.get("ADDRESS", "N/A")
            result["city"] = data.get("CITY", "N/A")
            result["district"] = data.get("DISTRICT", "N/A")
            result["state"] = data.get("STATE", "N/A")
            result["centre"] = data.get("CENTRE", "N/A")
            result["contact"] = data.get("CONTACT", "N/A")
            result["micr_code"] = data.get("MICR", "N/A")
            result["swift_code"] = data.get("SWIFT", None)
            result["iso3166"] = data.get("ISO3166", "N/A")
            result["imps_available"] = data.get("IMPS", False)
            result["neft_available"] = data.get("NEFT", False)
            result["rtgs_available"] = data.get("RTGS", False)
            result["upi_available"] = data.get("UPI", False)
            result["checked_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            result["api_info"] = {
                "developed_by": "Creator Shyamchand & Ayan",
                "organization": "CEO & Founder Of - Nexxon Hackers",
                "version": "1.0.0"
            }
            
            return result
        else:
            return {
                "success": False,
                "error": f"IFSC code not found or invalid",
                "ifsc_code": ifsc_code
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "ifsc_code": ifsc_code
        }

# ---------------- API ROUTES ----------------
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/ifsc/<ifsc_code>")
def api_ifsc(ifsc_code):
    result = get_ifsc_details(ifsc_code)
    
    # Ensure copyright is always present
    if "api_info" not in result and result.get("success"):
        result["api_info"] = {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    
    status_code = 200 if result.get("success") else 400
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=2),
        mimetype='application/json',
        status=status_code
    )

@app.route("/api/batch", methods=["POST"])
def api_batch():
    try:
        data = request.get_json()
        
        if not data or "ifsc_codes" not in data:
            return jsonify({
                "success": False,
                "error": "Please provide JSON with 'ifsc_codes' array",
                "example": {"ifsc_codes": ["SBIN0009174", "HDFC0000123"]}
            }), 400
        
        ifsc_codes = data["ifsc_codes"][:10]  # Limit to 10
        results = []
        
        for code in ifsc_codes:
            results.append(get_ifsc_details(code))
        
        return jsonify({
            "success": True,
            "total_requested": len(ifsc_codes),
            "total_found": sum(1 for r in results if r.get("success")),
            "results": results,
            "checked_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "api_info": {
                "developed_by": "Creator Shyamchand & Ayan",
                "organization": "CEO & Founder Of - Nexxon Hackers"
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Endpoint not found. Use /api/ifsc/{IFSC_CODE}",
        "available_endpoints": ["/", "/api/ifsc/{IFSC_CODE}", "/api/batch"],
        "api_info": {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    }), 404

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
