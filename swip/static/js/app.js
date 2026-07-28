// Translations
const translations = {
    en: {
        nav_home: "Home", nav_advisor: "Irrigation Advisor", nav_history: "History", nav_analytics: "Analytics",
        nav_about: "About SWIP", nav_features: "Features", nav_water: "Water Management", nav_gallery: "Gallery",
        home_title: "Smart Water Intelligence Platform",
        home_desc: "AI-Powered Water Intelligence for Sustainable Agriculture in Tajikistan",
        home_subtitle: "Data-Driven Agriculture", home_cta: "Get Recommendation",
        advisor_title: "Irrigation Advisor",
        lbl_temp: "Temperature (°C)", lbl_rain: "Rainfall (mm)", lbl_humidity: "Humidity (%)",
        lbl_soil_moisture: "Soil Moisture (%)", lbl_crop: "Crop Type", lbl_soil: "Soil Type",
        lbl_field_size: "Field Size (Hectares)", btn_predict: "Analyze Data",
        res_recommendation: "Recommendation", res_risk: "Risk Score", res_water: "Water Required",
        res_reasons: "AI Explanation",
        history_title: "Prediction History", th_date: "Date", th_crop: "Crop", th_moisture: "Moisture",
        th_prediction: "Recommendation", th_risk: "Risk",
        analytics_title: "Analytics Dashboard", chart_risk_trend: "Risk Score Trend", 
        chart_crop_dist: "Crop Distribution", chart_water_usage: "Estimated Water Required Over Time",
        crop_cotton: "Cotton", crop_wheat: "Wheat", crop_tomato: "Tomato", crop_potato: "Potato", crop_onion: "Onion", crop_cucumber: "Cucumber",
        soil_sandy: "Sandy", soil_loamy: "Loamy", soil_clay: "Clay",
        badge_irrigate: "IRRIGATE", badge_do_not_irrigate: "DO NOT IRRIGATE",
        hist_irrigate: "Irrigate", hist_do_not_irrigate: "Do Not Irrigate", lbl_liters: "Liters",
        about_title: "About SWIP",
        about_desc: "Smart Water Intelligence Platform (SWIP) is a cutting-edge artificial intelligence platform designed to address sustainable water management, optimize agricultural yields, and monitor the environment in Tajikistan. By integrating state-of-the-art machine learning models with real-time weather forecasting and sensor datasets, SWIP enables data-driven decision-making for farmers, agricultural specialists, and environmental managers.",
        mission_title: "Our Mission",
        mission_desc: "To empower farmers and communities with intelligent water management solutions for a sustainable future.",
        features_title: "Platform Features",
        feat_prediction_title: "AI Irrigation Advisor",
        feat_prediction_desc: "Analyzes soil moisture, humidity, temperature, and crop type to determine exactly when and how much to irrigate.",
        feat_risk_title: "Real-Time Risk Analysis",
        feat_risk_desc: "Monitors climate hazards and calculates risk indicators to prevent under-watering, crop failure, and soil erosion.",
        feat_analytics_title: "Water Usage Analytics",
        feat_analytics_desc: "Aggregates historical datasets and forecasts trends for comprehensive water consumption and budgeting.",
        feat_tajikistan_title: "Regional Focus",
        feat_tajikistan_desc: "Tailored specifically to Tajikistan's river basins, mountainous terrain, and cotton/wheat agricultural cycles.",
        water_title: "Water Management Hub",
        water_desc: "Sustainable water management is the key to Tajikistan's agricultural future. Efficient irrigation is particularly critical for cotton plantations, which require careful water budgeting to thrive without depleting regional reservoirs.",
        reservoir_status_title: "Nurek Reservoir & Lake Basin Status",
        reservoir_volume: "Active Volume: 10.5 Billion m³",
        reservoir_inflow: "Average Inflow: 640 m³/s",
        reservoir_outflow: "Average Outflow: 580 m³/s",
        water_saving_tips_title: "Irrigation Best Practices",
        tip1: "Schedule watering during early morning or late evening hours to minimize evaporation losses.",
        tip2: "Maintain optimal soil moisture levels based on crop-specific AI predictions to avoid water logging.",
        tip3: "In cotton fields, prefer drip irrigation or furrow wetting techniques to conserve up to 35% more water.",
        
        // Mockup translations
        btn_start_analysis: "Start Analysis",
        btn_learn_more: "Learn More",
        feat_smart_irrigation: "Smart Irrigation",
        feat_ai_forecasting: "AI Forecasting",
        feat_risk_detection: "Risk Detection",
        feat_water_optimization: "Water Optimization",
        insights_title_panel: "Crop Insights",
        insights_subtitle_panel: "Cotton Field Analysis",
        insights_desc_panel: "Monitor crop health, soil moisture, and yield predictions.",
        rec_actions_header: "Recommended Actions",
        act_optimize: "Optimize irrigation schedule",
        act_pest: "Monitor regional pest risks",
        act_soil: "Improve soil macronutrients",
        btn_view_details: "View Details",
        dash_water_cons: "Water Consumption",
        dash_field_health: "Field Health",
        dash_risk_score: "Risk Score",
        dash_good: "Good",
        dash_low_risk: "Low Risk",
        dash_pred_confidence: "Prediction Confidence",
        dash_high: "High",
        gallery_title: "Tajikistan Landscapes",
        photo1_title: "1. Pamir Valley",
        photo2_title: "2. Green Hills",
        photo3_title: "3. Reservoir / Lake",
        photo4_title: "4. Cotton Field",
        tag_hero: "Hero Background",
        tag_about: "About & Features",
        tag_dashboard: "Dashboard Banner",
        tag_advisor: "Advisor & Insights"
    },
    ru: {
        nav_home: "Главная", nav_advisor: "Советник по поливу", nav_history: "История", nav_analytics: "Аналитика",
        nav_about: "О платформе", nav_features: "Возможности", nav_water: "Управление водой", nav_gallery: "Галерея",
        home_title: "Интеллектуальная платформа водопользования",
        home_desc: "Интеллектуальное управление водными ресурсами на основе ИИ для устойчивого сельского хозяйства в Таджикистане",
        home_subtitle: "Сельское хозяйство на основе данных", home_cta: "Получить рекомендацию",
        advisor_title: "Советник по поливу",
        lbl_temp: "Температура (°C)", lbl_rain: "Осадки (мм)", lbl_humidity: "Влажность (%)",
        lbl_soil_moisture: "Влажность почвы (%)", lbl_crop: "Тип культуры", lbl_soil: "Тип почвы",
        lbl_field_size: "Размер поля (Гектары)", btn_predict: "Анализировать данные",
        res_recommendation: "Рекомендация", res_risk: "Уровень риска", res_water: "Требуется воды",
        res_reasons: "Объяснение ИИ",
        history_title: "История прогнозов", th_date: "Дата", th_crop: "Культура", th_moisture: "Влажность",
        th_prediction: "Рекомендация", th_risk: "Риск",
        analytics_title: "Аналитическая панель", chart_risk_trend: "Тенденция риска", 
        chart_crop_dist: "Распределение культур", chart_water_usage: "Потребление воды со временем",
        crop_cotton: "Хлопок", crop_wheat: "Пшеница", crop_tomato: "Томат", crop_potato: "Картофель", crop_onion: "Лук", crop_cucumber: "Огурец",
        soil_sandy: "Песчаная", soil_loamy: "Суглинистая", soil_clay: "Глинистая",
        badge_irrigate: "ПОЛИВАТЬ", badge_do_not_irrigate: "НЕ ПОЛИВАТЬ",
        hist_irrigate: "Поливать", hist_do_not_irrigate: "Не поливать", lbl_liters: "Литры",
        about_title: "О платформе SWIP",
        about_desc: "Smart Water Intelligence Platform (SWIP) — это передовая платформа искусственного интеллекта, разработанная для устойчивого управления водными ресурсами, оптимизации урожайности и экологического мониторинга в Таджикистане. Объединяя современные модели машинного обучения с прогнозами погоды в реальном времени и данными датчиков, SWIP позволяет фермерам и агрономам принимать решения на основе данных.",
        mission_title: "Наша миссия",
        mission_desc: "Предоставить фермерам и сообществам интеллектуальные решения для сохранения воды и устойчивого развития.",
        features_title: "Возможности платформы",
        feat_prediction_title: "Советник по поливу ИИ",
        feat_prediction_desc: "Анализирует влажность почвы, температуру и тип культуры для определения точных объемов полива.",
        feat_risk_title: "Анализ рисков в реальном времени",
        feat_risk_desc: "Мониторит климатические риски и рассчитывает показатели для предотвращения засухи и эрозии почв.",
        feat_analytics_title: "Аналитика потребления воды",
        feat_analytics_desc: "Агрегирует исторические данные и прогнозирует тренды расхода воды для планирования бюджета.",
        feat_tajikistan_title: "Региональный фокус",
        feat_tajikistan_desc: "Разработано с учетом речных бассейнов, горного рельефа и циклов выращивания хлопка и пшеницы в Таджикистане.",
        water_title: "Центр управления водными ресурсами",
        water_desc: "Эффективное управление водными ресурсами является ключом к будущему сельского хозяйства Таджикистана. Рациональное орошение особенно критично для хлопковых плантаций, требующих точного распределения воды.",
        reservoir_status_title: "Состояние Нурекского водохранилища",
        reservoir_volume: "Активный объем: 10.5 млрд м³",
        reservoir_inflow: "Средний приток: 640 м³/с",
        reservoir_outflow: "Средний отток: 580 м³/с",
        water_saving_tips_title: "Рекомендации по поливу",
        tip1: "Планируйте полив ранним утром или поздним вечером для снижения потерь от испарения.",
        tip2: "Поддерживайте оптимальную влажность почвы на основе рекомендаций ИИ, избегая переувлажнения.",
        tip3: "На хлопковых полях используйте капельное орошение для экономии до 35% воды.",
        
        // Mockup translations
        btn_start_analysis: "Начать анализ",
        btn_learn_more: "Подробнее",
        feat_smart_irrigation: "Умный полив",
        feat_ai_forecasting: "Прогноз ИИ",
        feat_risk_detection: "Анализ риска",
        feat_water_optimization: "Сбережение воды",
        insights_title_panel: "Анализ культур",
        insights_subtitle_panel: "Анализ хлопковых полей",
        insights_desc_panel: "Мониторинг здоровья культур, влажности почвы и прогнозирование урожая.",
        rec_actions_header: "Рекомендуемые действия",
        act_optimize: "Оптимизировать график полива",
        act_pest: "Мониторить угрозу вредителей",
        act_soil: "Улучшить макроэлементы почвы",
        btn_view_details: "Посмотреть детали",
        dash_water_cons: "Потребление воды",
        dash_field_health: "Здоровье поля",
        dash_risk_score: "Уровень риска",
        dash_good: "Хорошо",
        dash_low_risk: "Низкий риск",
        dash_pred_confidence: "Точность прогноза",
        dash_high: "Высокая",
        gallery_title: "Пейзажи Таджикистана",
        photo1_title: "1. Памирская долина",
        photo2_title: "2. Зеленые холмы",
        photo3_title: "3. Водохранилище / Озеро",
        photo4_title: "4. Хлопковое поле",
        tag_hero: "Главный фон",
        tag_about: "О платформе",
        tag_dashboard: "Панель управления",
        tag_advisor: "Советник и советы"
    },
    tg: {
        nav_home: "Асосӣ", nav_advisor: "Машваратчии обёрӣ", nav_history: "Таърих", nav_analytics: "Таҳлил",
        nav_about: "Дар бораи мо", nav_features: "Имкониятҳо", nav_water: "Идоракунии об", nav_gallery: "Аксҳо",
        home_title: "Платформаи зеҳнии истифодаи об",
        home_desc: "Идоракунии об бо зеҳни сунъӣ барои кишоварзии устувори Тоҷикистон",
        home_subtitle: "Кишоварзӣ дар асоси маълумот", home_cta: "Тавсия гиред",
        advisor_title: "Машваратчии обёрӣ",
        lbl_temp: "Ҳарорат (°C)", lbl_rain: "Боришот (мм)", lbl_humidity: "Намнокӣ (%)",
        lbl_soil_moisture: "Намнокии хок (%)", lbl_crop: "Намуди зироат", lbl_soil: "Намуди хок",
        lbl_field_size: "Андозаи майдон (Гектар)", btn_predict: "Таҳлил",
        res_recommendation: "Тавсия", res_risk: "Дараҷаи хавф", res_water: "Оби лозим",
        res_reasons: "Шарҳи AI",
        history_title: "Таърихи пешгӯиҳо", th_date: "Сана", th_crop: "Зироат", th_moisture: "Намнокӣ",
        th_prediction: "Тавсия", th_risk: "Хавф",
        analytics_title: "Панели таҳлил", chart_risk_trend: "Тамоюли хавф", 
        chart_crop_dist: "Тақсимоти зироат", chart_water_usage: "Истифодаи об",
        crop_cotton: "Пахта", crop_wheat: "Гандум", crop_tomato: "Помидор", crop_potato: "Картошка", crop_onion: "Пиёз", crop_cucumber: "Бодиринг",
        soil_sandy: "Регӣ", soil_loamy: "Хокӣ", soil_clay: "Гилӣ",
        badge_irrigate: "ОБЁРӢ КУНЕД", badge_do_not_irrigate: "ОБЁРӢ НАКУНЕД",
        hist_irrigate: "Обёрӣ кунед", hist_do_not_irrigate: "Обёрӣ накунед", lbl_liters: "Литр",
        about_title: "Дар бораи SWIP",
        about_desc: "Smart Water Intelligence Platform (SWIP) як платформаи муосири зеҳни сунъӣ мебошад, ки барои идоракунии устувори об, оптимизатсияи ҳосили зироатҳо ва мониторинги экологии Тоҷикистон пешбинӣ шудааст. Бо муттаҳид кардани моделҳои пешрафтаи омӯзиши мошин бо пешгӯиҳои обу ҳаво ва маълумоти сенсорӣ, SWIP ба деҳқонон ва агрономҳо имкон медиҳад, ки қарорҳои асоснок қабул кунанд.",
        mission_title: "Аввалиндараҷаи мо",
        mission_desc: "Таъмин кардани кишоварзон ва ҷомеаҳо бо қарорҳои ҳушманди об барои ояндаи устувор.",
        features_title: "Имкониятҳои платформа",
        feat_prediction_title: "Машваратчии обёрии AI",
        feat_prediction_desc: "Намнокӣ, ҳарорат ва намуди зироатро таҳлил карда, ҳаҷми дақиқи обёриро муайян мекунад.",
        feat_risk_title: "Таҳлили хавф дар вақти воқеӣ",
        feat_risk_desc: "Хатарҳои иқлимиро назорат карда, нишондиҳандаҳоро барои пешгирии хушксолӣ ва эрозияи хок ҳисоб мекунад.",
        feat_analytics_title: "Таҳлили истифодаи об",
        feat_analytics_desc: "Маълумоти таърихиро ҷамъ оварда, тамоюли истеъмоли обро барои банақшагирии буҷет пешгӯӣ мекунад.",
        feat_tajikistan_title: "Таваҷҷуҳи минтақавӣ",
        feat_tajikistan_desc: "Махсус барои ҳавзаҳои дарёҳо, релефи кӯҳсор ва давраҳои парвариши пахтаву гандум дар Тоҷикистон тарҳрезӣ шудааст.",
        water_title: "Маркази идоракунии об",
        water_desc: "Идоракунии устувори об калиди ояндаи кишоварзии Тоҷикистон аст. Обёрии самаранок махсусан барои киштзорҳои пахта муҳим аст, ки банақшагирии дақиқи обро талаб мекунад.",
        reservoir_status_title: "Ҳолати обанбори Норак",
        reservoir_volume: "Ҳаҷми фаъол: 10.5 миллиард м³",
        reservoir_inflow: "Вуруди миёна: 640 м³/с",
        reservoir_outflow: "Хуруҷи миёна: 580 м³/с",
        water_saving_tips_title: "Тавсияҳои обёрӣ",
        tip1: "Обёриро субҳи барвақт ё бегоҳирӯзӣ ба нақша гиред, то бухоршавии об кам шавад.",
        tip2: "Намнокии оптималии хокро дар асоси пешгӯиҳои AI нигоҳ доред, то аз ҳад зиёд об додани замин пешгирӣ шавад.",
        tip3: "Дар киштзорҳои пахта обёрии қатрагиро истифода баред, то то 35% обро сарфа кунед.",
        
        // Mockup translations
        btn_start_analysis: "Оғози таҳлил",
        btn_learn_more: "Муфассалтар",
        feat_smart_irrigation: "Обёрии ҳушманд",
        feat_ai_forecasting: "Пешгӯии ИИ",
        feat_risk_detection: "Анализи хавф",
        feat_water_optimization: "Сарфаи об",
        insights_title_panel: "Таҳлили зироат",
        insights_subtitle_panel: "Таҳлили майдони пахта",
        insights_desc_panel: "Назорати саломатии зироат, намнокии хок ва пешгӯии ҳосил.",
        rec_actions_header: "Амалҳои тавсияшуда",
        act_optimize: "Оптимизатсияи ҷадвали обёрӣ",
        act_pest: "Назорати хатари зараррасонҳо",
        act_soil: "Беҳтар кардани макроэлементҳои хок",
        btn_view_details: "Дидани тафсилот",
        dash_water_cons: "Истеъмоли об",
        dash_field_health: "Саломатии замин",
        dash_risk_score: "Хавфи хавф",
        dash_good: "Хуб",
        dash_low_risk: "Хавфи паст",
        dash_pred_confidence: "Боварии пешгӯӣ",
        dash_high: "Баланд",
        gallery_title: "Манзараҳои Тоҷикистон",
        photo1_title: "1. Водии Помир",
        photo2_title: "2. Таллаҳои сабз",
        photo3_title: "3. Обанбор / Кӯл",
        photo4_title: "4. Майдони пахта",
        tag_hero: "Фони асосӣ",
        tag_about: "Дар бораи мо",
        tag_dashboard: "Панели назорат",
        tag_advisor: "Машваратчӣ ва маслиҳат"
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Set Dashboard Date dynamic text (Sub-picture 3)
    updateDashboardDate();

    // Navigation
    const navLinks = document.querySelectorAll('.nav-links li');
    const sections = document.querySelectorAll('.page-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            const targetId = link.getAttribute('data-target');
            sections.forEach(sec => sec.classList.remove('active'));
            
            const targetSection = document.getElementById(targetId);
            targetSection.classList.add('active');

            // Trigger slow background zoom transition on homepage reactivation
            if (targetId === 'home') {
                targetSection.classList.remove('active-zoom');
                setTimeout(() => { targetSection.classList.add('active-zoom'); }, 50);
            } else {
                document.getElementById('home').classList.remove('active-zoom');
            }

            if(targetId === 'history') loadHistory();
            if(targetId === 'analytics') loadAnalytics();
            
            // Re-render Lucide icons inside loaded sections
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        });
    });

    // CTA Click events redirecting sections
    document.getElementById('start-analysis-btn').addEventListener('click', () => {
        document.querySelector('[data-target="advisor"]').click();
    });

    document.getElementById('learn-more-btn').addEventListener('click', () => {
        document.querySelector('[data-target="about"]').click();
    });

    document.getElementById('about-learn-more-btn').addEventListener('click', () => {
        document.querySelector('[data-target="features"]').click();
    });

    // Language selector
    document.getElementById('lang-select').addEventListener('change', (e) => {
        const lang = e.target.value;
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if(translations[lang][key]) {
                // If it contains icons, we must preserve icon tags or re-run lucide
                const hasIcon = el.querySelector('i');
                if (hasIcon) {
                    const iconName = hasIcon.getAttribute('data-lucide');
                    el.innerHTML = `<i data-lucide="${iconName}" class="nav-icon"></i><span>${translations[lang][key]}</span>`;
                } else {
                    el.innerText = translations[lang][key];
                }
            }
        });
        
        // Refresh dynamic date string based on language selector
        updateDashboardDate();
        
        // Refresh history table language if it's open
        if(document.getElementById('history').classList.contains('active')) {
            loadHistory();
        }
        // Refresh analytics if it's open
        if(document.getElementById('analytics').classList.contains('active')) {
            loadAnalytics();
        }
        // Update Results badge if shown
        if(document.getElementById('results-container').style.display === 'block') {
            const badge = document.getElementById('prediction-badge');
            if(badge.classList.contains('irrigate')) {
                badge.innerText = translations[lang].badge_irrigate;
            } else {
                badge.innerText = translations[lang].badge_do_not_irrigate;
            }
        }

        // Re-render icons after DOM language replace
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    });

    // Form Submit
    document.getElementById('prediction-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            temperature: parseFloat(document.getElementById('temperature').value),
            rainfall: parseFloat(document.getElementById('rainfall').value),
            humidity: parseFloat(document.getElementById('humidity').value),
            soil_moisture: parseFloat(document.getElementById('soil_moisture').value),
            field_size: parseFloat(document.getElementById('field_size').value),
            crop_type: document.getElementById('crop_type').value,
            soil_type: document.getElementById('soil_type').value,
            language: document.getElementById('lang-select').value
        };

        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        showResults(data);
    });
    
    // Auto-trigger slow zoom on initial load
    setTimeout(() => {
        document.getElementById('home').classList.add('active-zoom');
    }, 100);
});

function updateDashboardDate() {
    const lang = document.getElementById('lang-select').value;
    const dateEl = document.getElementById('dash-current-date');
    if (!dateEl) return;
    
    const now = new Date();
    let locale = 'en-US';
    if (lang === 'ru') locale = 'ru-RU';
    if (lang === 'tg') locale = 'tg-TJ'; // Note: Node/Browser fallback to Russian/English if Tajik locale data not loaded, but fallback is clean
    
    const formatted = now.toLocaleDateString(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    dateEl.innerText = formatted;
}

function showResults(data) {
    const container = document.getElementById('results-container');
    container.style.display = 'block';
    
    // Smooth fade in
    setTimeout(() => { container.style.opacity = '1'; }, 50);

    const lang = document.getElementById('lang-select').value;
    const badge = document.getElementById('prediction-badge');
    if(data.prediction === 1) {
        badge.innerText = translations[lang].badge_irrigate;
        badge.className = "badge irrigate";
    } else {
        badge.innerText = translations[lang].badge_do_not_irrigate;
        badge.className = "badge do-not-irrigate";
    }

    document.getElementById('risk-val').innerText = data.risk_score;
    const rl = document.getElementById('risk-level');
    rl.innerText = data.risk_level;
    rl.className = `metric-level level-${data.risk_level}`;

    document.getElementById('water-val').innerHTML = `${data.water_required_liters} <span style="font-size:14px;font-weight:normal">L</span>`;

    const reasonsList = document.getElementById('reasons-list');
    reasonsList.innerHTML = '';
    data.reasons.forEach(r => {
        const li = document.createElement('li');
        li.innerText = r;
        reasonsList.appendChild(li);
    });
}

async function loadHistory() {
    const res = await fetch('/api/history');
    const data = await res.json();
    const tbody = document.querySelector('#history-table tbody');
    tbody.innerHTML = '';

    const lang = document.getElementById('lang-select').value;

    data.history.forEach(row => {
        const tr = document.createElement('tr');
        const date = new Date(row.timestamp).toLocaleDateString();
        const predClass = row.prediction === 1 ? 'irrigate' : 'do-not-irrigate';
        const predText = row.prediction === 1 ? translations[lang].hist_irrigate : translations[lang].hist_do_not_irrigate;
        
        const cropKey = 'crop_' + row.crop_type.toLowerCase();
        const translatedCrop = translations[lang][cropKey] || row.crop_type;
        
        tr.innerHTML = `
            <td>${date}</td>
            <td>${translatedCrop}</td>
            <td>${row.soil_moisture.toFixed(1)}%</td>
            <td><span class="badge ${predClass}" style="padding: 2px 8px; font-size: 12px;">${predText}</span></td>
            <td><span class="metric-level level-${row.risk_score > 70 ? 'HIGH' : (row.risk_score > 30 ? 'MEDIUM' : 'LOW')}">${row.risk_score}</span></td>
        `;
        tbody.appendChild(tr);
    });
}
