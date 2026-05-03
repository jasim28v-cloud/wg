def generate_html(servers_json, stats_json, servers_by_protocol, total_servers, new_count, deleted_count, avg_ping, most_country, most_country_count, active_count, idle_count, warning_count, update_time_str, update_date_str, current_time_iso, max_age_hours, greetings_json, welcome_msg, subtitle_msg):
    
    filter_tabs_html = f'''
    <button class="tab-btn active px-4 py-2 rounded-full text-xs font-medium" data-filter="all">
        <i class="fas fa-globe ml-1"></i> الكل (<span id="count-all">{total_servers}</span>)
    </button>
    <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" data-filter="active">
        🟢 نشط (<span id="count-active">{active_count}</span>)
    </button>'''
    
    for proto_key, proto_name, icon in [
        ("vmess", "VMess", "🟠"), ("vless", "VLESS", "🔵"),
        ("trojan", "Trojan", "🟣"), ("ss", "SS", "🟢"),
        ("ssh", "SSH", "🔒"), ("hysteria2", "Hysteria2", "🩷")
    ]:
        count = len(servers_by_protocol.get(proto_key, []))
        if count > 0:
            filter_tabs_html += f'''
    <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" data-filter="{proto_key}">
        {icon} {proto_name} (<span id="count-{proto_key}">{count}</span>)
    </button>'''
    
    filter_tabs_html += '''
            <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" id="fav-filter-btn" data-filter="favorites" style="display:none;">
                ⭐ المفضلة (<span id="count-fav">0</span>)
            </button>'''
    
    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOKA Exclave VPN | Ultra Glass</title>
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#0f0c29">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --aurora-1: rgba(99, 102, 241, 0.15);
            --aurora-2: rgba(236, 72, 153, 0.1);
            --aurora-3: rgba(34, 197, 94, 0.08);
            --aurora-4: rgba(168, 85, 247, 0.12);
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-hover: rgba(255, 255, 255, 0.06);
            --neon-glow: 0 0 30px rgba(99, 102, 241, 0.3);
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: 'Tajawal', sans-serif;
            background: #06060f;
            min-height: 100vh;
            color: #e2e8f0;
            position: relative;
            overflow-x: hidden;
        }}
        
        /* ============ AURORA BACKGROUND ============ */
        .aurora-container {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }}
        .aurora {{
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.6;
            animation: auroraFloat 20s ease-in-out infinite;
        }}
        .aurora-1 {{
            width: 70vw; height: 70vw;
            background: radial-gradient(circle, var(--aurora-1) 0%, transparent 70%);
            top: -25%; left: -15%;
            animation-delay: 0s;
        }}
        .aurora-2 {{
            width: 60vw; height: 60vw;
            background: radial-gradient(circle, var(--aurora-2) 0%, transparent 70%);
            bottom: -20%; right: -10%;
            animation-delay: -7s;
        }}
        .aurora-3 {{
            width: 50vw; height: 50vw;
            background: radial-gradient(circle, var(--aurora-3) 0%, transparent 70%);
            top: 40%; left: 30%;
            animation-delay: -14s;
        }}
        .aurora-4 {{
            width: 45vw; height: 45vw;
            background: radial-gradient(circle, var(--aurora-4) 0%, transparent 70%);
            bottom: 10%; left: 5%;
            animation-delay: -3s;
        }}
        @keyframes auroraFloat {{
            0%, 100% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
            25% {{ transform: translate(40px, -30px) scale(1.1) rotate(5deg); }}
            50% {{ transform: translate(-20px, 25px) scale(0.95) rotate(-3deg); }}
            75% {{ transform: translate(-35px, -15px) scale(1.05) rotate(2deg); }}
        }}
        
        /* ============ FLOATING NEON ORBS ============ */
        .orbs-container {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }}
        .orb {{
            position: absolute;
            border-radius: 50%;
            animation: orbFloat linear infinite;
        }}
        @keyframes orbFloat {{
            0% {{ transform: translateY(105vh) scale(0); opacity: 0; }}
            5% {{ opacity: 0.8; }}
            95% {{ opacity: 0.8; }}
            100% {{ transform: translateY(-10vh) scale(1.2); opacity: 0; }}
        }}
        
        /* ============ GLASS PANELS ============ */
        .glass {{
            background: var(--glass-bg);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            border: 1px solid var(--glass-border);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.05);
        }}
        .glass-card {{
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(30px) saturate(180%);
            -webkit-backdrop-filter: blur(30px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 28px;
            transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
            opacity: 0;
            transform: translateY(40px) scale(0.95);
            position: relative;
            overflow: hidden;
        }}
        .glass-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 50%);
            pointer-events: none;
            border-radius: 28px;
        }}
        .glass-card.visible {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
        .glass-card:hover {{
            background: var(--glass-hover);
            border-color: rgba(255, 255, 255, 0.15);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5), var(--neon-glow);
            transform: translateY(-8px) scale(1.03);
        }}
        .glass-card.new-server {{
            animation: newPulse 2.5s ease-in-out infinite;
        }}
        @keyframes newPulse {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.5), 0 0 0 0 rgba(34, 197, 94, 0.3); }}
            50% {{ box-shadow: 0 0 40px 10px rgba(34, 197, 94, 0.15), 0 0 80px 20px rgba(34, 197, 94, 0.05); }}
        }}
        
        /* ============ NAVIGATION ============ */
        .glass-nav {{
            background: rgba(6, 6, 15, 0.5);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }}
        
        /* ============ TABS ============ */
        .tab-btn {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            color: #94a3b8;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
            backdrop-filter: blur(10px);
        }}
        .tab-btn:hover {{
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.15);
            color: #e2e8f0;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
        }}
        .tab-btn.active {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(139, 92, 246, 0.3));
            border-color: rgba(139, 92, 246, 0.5);
            color: white;
            box-shadow: 0 0 40px rgba(99, 102, 241, 0.4), 0 0 80px rgba(99, 102, 241, 0.2);
        }}
        
        /* ============ BUTTONS ============ */
        .btn-primary {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.6), rgba(139, 92, 246, 0.6));
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
            backdrop-filter: blur(10px);
        }}
        .btn-primary:hover {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8));
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 40px rgba(99, 102, 241, 0.5), 0 0 60px rgba(139, 92, 246, 0.3);
            transform: translateY(-3px);
        }}
        .btn-glass {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #e2e8f0;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
            backdrop-filter: blur(10px);
        }}
        .btn-glass:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.2);
        }}
        
        /* ============ BADGES ============ */
        .badge-new {{
            background: linear-gradient(135deg, #22c55e, #10b981);
            color: white;
            font-size: 0.6rem;
            font-weight: 800;
            padding: 3px 10px;
            border-radius: 30px;
            animation: badgeGlow 2s ease-in-out infinite;
            box-shadow: 0 0 20px rgba(34, 197, 94, 0.4);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        @keyframes badgeGlow {{
            0%, 100% {{ box-shadow: 0 0 10px rgba(34, 197, 94, 0.4); }}
            50% {{ box-shadow: 0 0 30px rgba(34, 197, 94, 0.8), 0 0 60px rgba(34, 197, 94, 0.3); }}
        }}
        .badge-active {{ background: rgba(34, 197, 94, 0.12); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }}
        .badge-idle {{ background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
        .badge-warning {{ background: rgba(249, 115, 22, 0.12); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.3); }}
        
        /* ============ FAVORITE STAR ============ */
        .favorite-star {{
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
            color: #475569;
            filter: drop-shadow(0 0 2px transparent);
        }}
        .favorite-star.active {{
            color: #fbbf24;
            filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.6));
            animation: starPop 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        }}
        @keyframes starPop {{
            0% {{ transform: scale(1); }}
            40% {{ transform: scale(1.5); }}
            100% {{ transform: scale(1); }}
        }}
        
        /* ============ SCROLLBAR ============ */
        ::-webkit-scrollbar {{ width: 4px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255, 255, 255, 0.06); border-radius: 10px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(255, 255, 255, 0.12); }}
        
        /* ============ TOAST ============ */
        .toast {{
            background: rgba(15, 15, 30, 0.8);
            backdrop-filter: blur(30px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 40px rgba(99, 102, 241, 0.2);
        }}
        
        /* ============ LINK PREVIEW ============ */
        .link-preview {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 18px;
            font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
        }}
        
        /* ============ CONFETTI ============ */
        .confetti {{
            position: fixed;
            pointer-events: none;
            z-index: 9999;
            animation: confettiFall 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        }}
        @keyframes confettiFall {{
            0% {{ transform: translateY(-100px) rotate(0deg) scale(1); opacity: 1; }}
            100% {{ transform: translateY(105vh) rotate(1080deg) scale(0.3); opacity: 0; }}
        }}
        
        /* ============ HERO STATS ============ */
        .stat-card {{
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 22px;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        }}
        .stat-card:hover {{
            border-color: rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), 0 0 30px rgba(99, 102, 241, 0.15);
            transform: translateY(-4px);
        }}
        
        .visitor-badge {{
            background: rgba(34, 197, 94, 0.08);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: 30px;
        }}
    </style>
</head>
<body class="antialiased relative z-10">

    <!-- AURORA BACKGROUND -->
    <div class="aurora-container">
        <div class="aurora aurora-1"></div>
        <div class="aurora aurora-2"></div>
        <div class="aurora aurora-3"></div>
        <div class="aurora aurora-4"></div>
    </div>

    <!-- FLOATING ORBS -->
    <div class="orbs-container" id="orbs"></div>

    <!-- NAVIGATION -->
    <nav class="glass-nav sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-5 py-4 flex flex-wrap justify-between items-center text-sm gap-4">
            <div class="flex items-center gap-4">
                <span class="text-3xl font-black bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 bg-clip-text text-transparent drop-shadow-lg">DOKA</span>
                <span class="hidden sm:inline w-px h-6 bg-white/10"></span>
                <span class="hidden sm:inline text-gray-400 text-xs tracking-wide">EXCLAVE VPN</span>
            </div>
            <div class="flex items-center gap-5 flex-wrap">
                <div class="flex items-center gap-2 text-gray-400 text-xs">
                    <span id="user-ip" class="font-mono text-gray-300 text-xs">...</span>
                    <span class="w-2 h-2 bg-red-500 rounded-full animate-pulse" style="box-shadow: 0 0 10px rgba(239,68,68,0.6);"></span>
                    <span class="text-red-400 font-bold text-xs tracking-wide">غير محمي</span>
                </div>
                <span class="w-px h-5 bg-white/10 hidden sm:block"></span>
                <div class="flex items-center gap-2 text-gray-400 text-xs">
                    <i class="far fa-clock text-indigo-400"></i>
                    <span id="live-clock" class="font-mono">--:--:--</span>
                    <span class="text-gray-600">·</span>
                    <span id="update-date" class="hidden sm:inline">{update_date_str}</span>
                </div>
                <div class="visitor-badge px-3 py-1.5 text-xs text-green-400 flex items-center gap-1.5">
                    <i class="fas fa-bolt text-green-400"></i>
                    <span id="visitor-count">--</span>
                </div>
            </div>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="relative py-16 md:py-24 text-center px-4">
        <div class="max-w-4xl mx-auto">
            <div class="inline-flex items-center gap-2 glass rounded-full px-5 py-2.5 text-xs text-gray-300 mb-8">
                <span class="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse" style="box-shadow: 0 0 15px rgba(34,197,94,0.6);"></span>
                <span id="countdown-next" class="font-mono">التحديث القادم بعد: --:--:--</span>
                <span class="text-gray-600">·</span>
                <span>⏳ {max_age_hours} ساعة</span>
            </div>
            
            <h1 class="text-5xl md:text-8xl font-black mb-6 leading-none tracking-tight">
                <span class="bg-gradient-to-r from-indigo-200 via-purple-200 to-pink-200 bg-clip-text text-transparent drop-shadow-2xl">
                    حرية التصفح
                </span>
            </h1>
            <p class="text-gray-400 text-lg md:text-xl mb-3 font-light tracking-wide" id="subtitle-message">{subtitle_msg}</p>
            <p class="text-gray-500 text-sm mb-2 opacity-80" id="welcome-message">{welcome_msg}</p>
            <p class="text-gray-500 text-sm mb-10 font-medium" id="greeting-message"></p>
            
            <!-- STATS CARDS -->
            <div class="flex flex-wrap justify-center gap-4 mb-6">
                <div class="stat-card px-6 py-4 text-center min-w-[100px]">
                    <span class="text-3xl md:text-4xl font-black bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">{total_servers}</span>
                    <p class="text-gray-500 text-[10px] mt-1.5 uppercase tracking-widest">سيرفر</p>
                </div>
                <div class="stat-card px-6 py-4 text-center min-w-[100px]">
                    <span class="text-3xl md:text-4xl font-black text-green-400" style="text-shadow: 0 0 30px rgba(34,197,94,0.5);">{active_count}</span>
                    <p class="text-gray-500 text-[10px] mt-1.5 uppercase tracking-widest">🟢 نشط</p>
                </div>
                <div class="stat-card px-6 py-4 text-center min-w-[100px]">
                    <span class="text-3xl md:text-4xl font-black text-amber-400">{idle_count}</span>
                    <p class="text-gray-500 text-[10px] mt-1.5 uppercase tracking-widest">💤 خامل</p>
                </div>
                <div class="stat-card px-6 py-4 text-center min-w-[100px]">
                    <span class="text-3xl md:text-4xl font-black text-orange-400">{warning_count}</span>
                    <p class="text-gray-500 text-[10px] mt-1.5 uppercase tracking-widest">⚠️ خطر</p>
                </div>
                <div class="stat-card px-6 py-4 text-center min-w-[100px]">
                    <span class="text-3xl md:text-4xl font-black text-emerald-400">{new_count}</span>
                    <p class="text-gray-500 text-[10px] mt-1.5 uppercase tracking-widest">🆕 جديد</p>
                </div>
                <div class="stat-card px-6 py-4 text-center min-w-[120px]">
                    <span class="text-xl md:text-2xl font-black text-cyan-400">{most_country}</span>
                    <p class="text-gray-500 text-[10px] mt-1.5 uppercase tracking-widest">🌍 الأكثر</p>
                </div>
            </div>
        </div>
    </section>

    <!-- FILTERS & SEARCH -->
    <section class="max-w-7xl mx-auto px-4 py-2">
        <div class="flex flex-wrap justify-center gap-2" id="filter-tabs">
            {filter_tabs_html}
        </div>
        <div class="flex justify-center mt-4">
            <div class="glass flex items-center gap-3 px-5 py-3 rounded-full max-w-md w-full">
                <i class="fas fa-search text-gray-500 text-sm"></i>
                <input type="text" id="search-input" placeholder="ابحث عن دولة أو بروتوكول..." class="bg-transparent border-none outline-none text-white text-sm w-full placeholder-gray-600">
                <button onclick="document.getElementById('search-input').value=''; renderServers(currentFilter);" class="text-gray-600 hover:text-white text-sm transition-colors">✕</button>
            </div>
        </div>
    </section>

    <!-- SERVERS GRID -->
    <section class="max-w-7xl mx-auto px-4 py-8">
        <h2 class="text-xl font-bold mb-6 text-gray-300 flex items-center gap-3">
            <i class="fas fa-server text-indigo-400"></i> 
            سيرفرات Exclave VPN
            <span class="text-xs text-gray-600 font-normal">· 🟢{active_count} 💤{idle_count} ⚠️{warning_count}</span>
            <span class="text-xs text-gray-600 font-normal" id="last-copied-info"></span>
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5" id="servers-grid"></div>
        <div id="no-servers-msg" class="text-center py-20 text-gray-600 hidden">
            <i class="fas fa-search text-4xl mb-4 opacity-20"></i>
            <p id="no-results-text" class="text-sm">لا توجد سيرفرات</p>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="border-t border-white/5 mt-16">
        <div class="max-w-7xl mx-auto px-4 py-10 text-center">
            <p class="text-gray-600 text-xs">© 2026 DOKA Exclave VPN · جميع الحقوق محفوظة</p>
            <p class="text-gray-700 text-[10px] mt-1.5">تحديث كل 3 ساعات · ⏳ حذف بعد {max_age_hours} ساعة</p>
            <button id="show-stats-btn" class="mt-5 glass px-6 py-2.5 rounded-full text-xs text-gray-400 hover:text-white transition-all duration-500 hover:border-indigo-400/30">
                <i class="fas fa-chart-pie ml-1.5"></i> الإحصائيات
            </button>
            <button id="clear-fav-btn" class="mt-3 block mx-auto text-[10px] text-gray-700 hover:text-red-400 transition-all" style="display:none;">
                <i class="fas fa-trash-alt ml-1"></i> حذف المفضلة
            </button>
        </div>
    </footer>

    <!-- STATS PAGE -->
    <div id="stats-page" class="max-w-4xl mx-auto px-4 py-16 hidden">
        <div class="glass-card p-8" style="opacity:1;transform:none;">
            <h2 class="text-3xl font-bold text-center mb-10">📊 لوحة الإحصائيات</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div><h3 class="text-base font-bold mb-4 text-gray-400">البروتوكولات</h3><canvas id="proto-chart"></canvas></div>
                <div><h3 class="text-base font-bold mb-4 text-gray-400">الدول</h3><canvas id="country-chart"></canvas></div>
            </div>
            <p class="text-center text-gray-500 mt-8 text-xs">آخر تحديث: <span id="stats-last-update" class="text-white"></span></p>
            <button id="back-to-servers" class="mt-8 btn-primary px-8 py-3 rounded-2xl mx-auto block text-sm font-medium">
                <i class="fas fa-arrow-right ml-2"></i> عودة للسيرفرات
            </button>
        </div>
    </div>

    <!-- TOAST -->
    <div id="toast" class="toast fixed bottom-8 left-1/2 -translate-x-1/2 px-8 py-4 rounded-2xl text-sm font-bold opacity-0 transition-all duration-500 pointer-events-none z-50 text-white" style="transform: translate(-50%, 30px);">
        <span id="toast-msg">تم النسخ!</span>
    </div>

    <!-- QR MODAL -->
    <div id="qr-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/70 backdrop-blur-sm" onclick="closeQRModal(event)">
        <div class="glass-card p-8" onclick="event.stopPropagation()" style="opacity:1;transform:none;">
            <div id="qr-modal-content" class="flex justify-center"></div>
            <button onclick="closeQRModal()" class="mt-6 w-full btn-primary py-3 rounded-xl text-sm font-medium">إغلاق</button>
        </div>
    </div>

    <script>
        const serversData = {servers_json};
        const statsData = {stats_json};
        const greetings = {greetings_json};
        const MAX_AGE_HOURS = {max_age_hours};
        let currentFilter = 'all';
        let chartInstances = {{}};
        const UPDATE_INTERVAL = 3 * 60 * 60;
        const updateTime = new Date('{current_time_iso}');
        
        // ==================== FAVORITES ====================
        function getFavorites() {{ try {{ return JSON.parse(localStorage.getItem('doka_exclave_fav') || '[]'); }} catch {{ return []; }} }}
        function saveFavorites(f) {{ localStorage.setItem('doka_exclave_fav', JSON.stringify(f)); }}
        function toggleFavorite(link) {{
            let f = getFavorites(); const i = f.indexOf(link);
            i > -1 ? (f.splice(i,1), showToast('أزيل من المفضلة 💔')) : (f.push(link), showToast('أضيف للمفضلة ⭐'));
            saveFavorites(f); renderServers(currentFilter); updateFavCount();
        }}
        function updateFavCount() {{
            const f = getFavorites(); document.getElementById('count-fav').textContent = f.length;
            const b = document.getElementById('fav-filter-btn'), c = document.getElementById('clear-fav-btn');
            if (f.length > 0) {{ b.style.display = ''; c.style.display = ''; }} else {{ b.style.display = 'none'; c.style.display = 'none'; }}
        }}
        
        // ==================== TOAST + CONFETTI ====================
        function showToast(m) {{
            const t = document.getElementById('toast'); document.getElementById('toast-msg').textContent = m;
            t.style.opacity = '1'; t.style.transform = 'translate(-50%, 0)';
            setTimeout(() => {{ t.style.opacity = '0'; t.style.transform = 'translate(-50%, 30px)'; }}, 2200);
        }}
        function spawnConfetti() {{
            const colors = ['#6366f1','#ec4899','#22c55e','#f59e0b','#3b82f6','#a855f7','#fbbf24','#06b6d4'];
            for (let i=0; i<40; i++) {{
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random()*100+'%';
                confetti.style.top = '-20px';
                confetti.style.width = Math.random()*10+4+'px';
                confetti.style.height = Math.random()*10+4+'px';
                confetti.style.background = colors[Math.floor(Math.random()*colors.length)];
                confetti.style.animationDuration = Math.random()*1.5+1+'s';
                confetti.style.animationDelay = Math.random()*0.4+'s';
                confetti.style.borderRadius = Math.random()>0.4 ? '50%' : '3px';
                document.body.appendChild(confetti);
                setTimeout(() => confetti.remove(), 2000);
            }}
        }}
        
        // ==================== COPY ====================
        window.copyText = (text) => {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast('✅ تم النسخ! 🎉');
                spawnConfetti();
                localStorage.setItem('doka_exclave_last_copy', text);
                updateLastCopied();
            }});
        }};
        function updateLastCopied() {{
            const l = localStorage.getItem('doka_exclave_last_copy');
            if (l) document.getElementById('last-copied-info').textContent = '· آخر نسخ: ' + l.substring(0, 25) + '...';
        }}
        
        // ==================== QR ====================
        window.showQR = (link) => {{
            const m = document.getElementById('qr-modal'), c = document.getElementById('qr-modal-content');
            c.innerHTML = ''; new QRCode(c, {{ text: link, width: 220, height: 220, colorDark: "#e2e8f0", colorLight: "#0f0f1a" }});
            m.classList.remove('hidden'); m.classList.add('flex');
        }};
        window.closeQRModal = (e) => {{
            if (e && e.target !== document.getElementById('qr-modal')) return;
            const m = document.getElementById('qr-modal'); m.classList.add('hidden'); m.classList.remove('flex');
            document.getElementById('qr-modal-content').innerHTML = '';
        }};
        
        // ==================== RENDER SERVERS ====================
        function renderServers(filter) {{
            const grid = document.getElementById('servers-grid');
            const s = document.getElementById('search-input').value.toLowerCase().trim();
            const favs = getFavorites();
            let filtered = serversData;
            
            if (filter === 'favorites') filtered = serversData.filter(srv => favs.includes(srv.link));
            else if (filter === 'active') filtered = serversData.filter(srv => srv.status === 'active');
            else if (filter !== 'all') filtered = serversData.filter(srv => srv.proto.toLowerCase() === filter);
            
            if (s) filtered = filtered.filter(srv => srv.country.includes(s) || srv.proto.toLowerCase().includes(s) || srv.link.toLowerCase().includes(s));
            
            if (filtered.length === 0) {{
                grid.innerHTML = '';
                document.getElementById('no-servers-msg').classList.remove('hidden');
                return;
            }}
            document.getElementById('no-servers-msg').classList.add('hidden');
            
            let h = '';
            filtered.forEach((srv, i) => {{
                const isFav = favs.includes(srv.link);
                const dl = srv.link.length > 50 ? srv.link.substring(0, 25) + ' ... ' + srv.link.substring(srv.link.length - 18) : srv.link;
                
                let statusBadge = '';
                if (srv.status === 'active') statusBadge = '<span class="badge-active text-[0.6rem] px-2.5 py-1 rounded-full font-bold">🟢 نشط</span>';
                else if (srv.status === 'idle') statusBadge = '<span class="badge-idle text-[0.6rem] px-2.5 py-1 rounded-full font-bold">💤 خامل</span>';
                else statusBadge = '<span class="badge-warning text-[0.6rem] px-2.5 py-1 rounded-full font-bold">⚠️ خطر</span>';
                
                h += `<div class="glass-card p-5 ${{srv.is_new ? 'new-server' : ''}}" style="animation-delay:${{i*0.07}}s;">
                    <div class="flex justify-between items-start mb-3">
                        <div class="flex items-center gap-2 flex-wrap">
                            <span class="text-3xl">${{srv.flag}}</span>
                            <span class="bg-gradient-to-r ${{srv.proto_gradient}} text-white text-[0.65rem] font-bold px-3 py-1 rounded-full uppercase tracking-wider">${{srv.proto}}</span>
                            ${{srv.is_new ? '<span class="badge-new">جديد</span>' : ''}}
                            ${{statusBadge}}
                        </div>
                        <div class="flex items-center gap-2">
                            <i class="favorite-star fa-star ${{isFav ? 'fas active' : 'far'}} text-lg" onclick="toggleFavorite('${{srv.link}}'); event.stopPropagation();"></i>
                            <span class="text-[10px] text-gray-500 font-mono">${{srv.ping}}ms</span>
                        </div>
                    </div>
                    <p class="text-[11px] text-gray-500 mb-3"><i class="fas fa-map-marker-alt ml-1 text-indigo-500"></i> ${{srv.country}} <span class="text-gray-700">· ${{srv.added_time}} · ${{srv.age_hours}}س</span></p>
                    <div class="link-preview p-3 mb-4 text-[11px] text-gray-400 break-all leading-relaxed" dir="ltr">${{dl}}</div>
                    <div class="flex gap-2">
                        <button onclick="copyText('${{srv.link}}')" class="flex-1 btn-primary py-2.5 rounded-xl text-xs font-semibold tracking-wide"><i class="far fa-copy ml-1.5"></i> نسخ</button>
                        <button onclick="showQR('${{srv.link}}')" class="btn-glass px-4 rounded-xl text-sm"><i class="fas fa-qrcode"></i></button>
                    </div>
                </div>`;
            }});
            grid.innerHTML = h;
            requestAnimationFrame(() => {{ document.querySelectorAll('.glass-card').forEach((c, i) => setTimeout(() => c.classList.add('visible'), i * 80)); }});
        }}
        
        // ==================== FILTERS ====================
        document.querySelectorAll('.tab-btn').forEach(b => b.addEventListener('click', () => {{
            document.querySelectorAll('.tab-btn').forEach(x => x.classList.remove('active'));
            b.classList.add('active'); currentFilter = b.dataset.filter; renderServers(currentFilter);
        }}));
        document.getElementById('search-input').addEventListener('input', () => renderServers(currentFilter));
        
        // ==================== CLOCK ====================
        function uc() {{ document.getElementById('live-clock').textContent = new Date().toLocaleTimeString('ar-IQ', {{ hour12: false }}); }}
        setInterval(uc, 1000); uc();
        
        // ==================== COUNTDOWN ====================
        function cd() {{
            const e = Math.floor((new Date() - updateTime) / 1000);
            const r = Math.max(0, UPDATE_INTERVAL - e);
            document.getElementById('countdown-next').textContent = `التحديث القادم بعد: ${{String(Math.floor(r/3600)).padStart(2,'0')}}:${{String(Math.floor((r%3600)/60)).padStart(2,'0')}}:${{String(r%60).padStart(2,'0')}}`;
        }}
        setInterval(cd, 1000); cd();
        
        // ==================== GREETINGS ====================
        document.getElementById('greeting-message').textContent = greetings[Math.floor(Math.random() * greetings.length)];
        setInterval(() => {{ document.getElementById('greeting-message').textContent = greetings[Math.floor(Math.random() * greetings.length)]; }}, 25000);
        
        // ==================== ORBS ====================
        (function() {{
            const co = document.getElementById('orbs');
            const cols = ['rgba(99,102,241,0.5)', 'rgba(236,72,153,0.4)', 'rgba(34,197,94,0.35)', 'rgba(168,85,247,0.4)', 'rgba(251,191,36,0.3)'];
            for (let i=0; i<20; i++) {{
                const orb = document.createElement('div'); orb.className = 'orb';
                const size = Math.random()*60+20;
                orb.style.cssText = `width:${{size}}px;height:${{size}}px;left:${{Math.random()*100}}%;background:${{cols[Math.floor(Math.random()*cols.length)]}};animation-duration:${{Math.random()*25+20}}s;animation-delay:${{Math.random()*20}}s;filter:blur(${{Math.random()*8+4}}px);`;
                co.appendChild(orb);
            }}
        }})();
        
        // ==================== VISITORS ====================
        function uv() {{ document.getElementById('visitor-count').textContent = Math.max(1, {total_servers} + Math.floor(Math.random()*20)-8); }}
        uv(); setInterval(uv, 12000);
        
        // ==================== STATS PAGE ====================
        document.getElementById('show-stats-btn').addEventListener('click', () => {{
            document.querySelector('nav').style.display='none';
            document.querySelector('section').style.display='none';
            document.getElementById('filter-tabs').style.display='none';
            document.getElementById('servers-grid').parentElement.style.display='none';
            document.querySelector('footer').style.display='none';
            document.querySelector('.aurora-container').style.display='none';
            document.querySelector('.orbs-container').style.display='none';
            document.getElementById('stats-page').classList.remove('hidden');
            document.getElementById('stats-last-update').textContent = new Date(statsData.last_updated).toLocaleString('ar-IQ');
            Object.values(chartInstances).forEach(c => c.destroy());
            chartInstances = {{}};
            
            const ctx1 = document.getElementById('proto-chart').getContext('2d');
            chartInstances.proto = new Chart(ctx1, {{
                type: 'doughnut',
                data: {{ labels: Object.keys(statsData.by_protocol).map(p=>p.toUpperCase()), datasets: [{{ data: Object.values(statsData.by_protocol), backgroundColor: ['#f97316','#3b82f6','#a855f7','#22c55e','#64748b','#f43f5e'], borderColor: 'rgba(255,255,255,0.05)', borderWidth: 4, hoverBorderColor: 'rgba(255,255,255,0.2)' }}] }},
                options: {{ responsive: true, plugins: {{ legend: {{ position:'bottom', labels: {{ color:'#94a3b8', padding:16, font:{{family:'Tajawal',size:11}} }} }} }}, cutout: '65%' }}
            }});
            
            const ctx2 = document.getElementById('country-chart').getContext('2d');
            const co2 = statsData.countries || {{}};
            chartInstances.country = new Chart(ctx2, {{
                type: 'polarArea',
                data: {{ labels: Object.keys(co2), datasets: [{{ data: Object.values(co2), backgroundColor: ['#6366f1','#ec4899','#22c55e','#f59e0b','#3b82f6','#ef4444','#a855f7','#06b6d4'], borderColor: 'rgba(255,255,255,0.05)', borderWidth: 3 }}] }},
                options: {{ responsive: true, plugins: {{ legend: {{ position:'bottom', labels: {{ color:'#94a3b8', padding:14, font:{{family:'Tajawal',size:10}} }} }} }}, scales: {{ r: {{ ticks: {{ display:false }}, grid: {{ color:'rgba(255,255,255,0.03)' }} }} }} }}
            }});
        }});
        
        document.getElementById('back-to-servers').addEventListener('click', () => location.reload());
        document.getElementById('clear-fav-btn').addEventListener('click', () => {{
            if (confirm('حذف كل المفضلة؟')) {{ localStorage.removeItem('doka_exclave_fav'); updateFavCount(); if (currentFilter==='favorites') renderServers('all'); else renderServers(currentFilter); showToast('تم حذف المفضلة 🗑️'); }}
        }});
        
        // ==================== INIT ====================
        fetch('https://api.ipify.org?format=json').then(r=>r.json()).then(d=>document.getElementById('user-ip').textContent=d.ip).catch(()=>document.getElementById('user-ip').textContent='غير معروف');
        updateFavCount(); updateLastCopied(); renderServers('all');
        
        console.log('%c🚀 DOKA EXCLAVE VPN %c| %cULTRA GLASS EDITION %c💎',
            'color:#818cf8;font-size:24px;font-weight:bold;',
            'color:#94a3b8;',
            'color:#c084fc;font-size:18px;',
            'color:#fbbf24;');
        console.log('%cصنع بحب 💛%c',
            'color:#fbbf24;font-size:14px;',
            '');
    </script>
</body>
</html>'''
    
    return html
