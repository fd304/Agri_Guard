// SWIP Application Logic — Full i18n + Weather Integration + Decision Engine v2.0

// ========== TRANSLATIONS ==========
const T = {
    en: {
        // Sidebar
        nav_subtitle: "Smart Water &\nIrrigation Platform",
        nav_dashboard: "Dashboard", nav_weather: "Weather", nav_predictor: "Predictor",
        nav_risk: "Risk Scorer", nav_water: "Water Management", nav_field: "Field & Soil",
        nav_analytics: "Analytics", nav_alerts: "Alerts", nav_reports: "Reports",
        nav_settings: "Settings", nav_help: "Help",
        // Topbar
        last_updated: "Last updated: --",
        // Dashboard
        dash_welcome: "Welcome back, Agri Guard",
        dash_desc: "Here is the current status of your fields based on live weather data.",
        kpi_water_need: "Water Need Today", kpi_water_stress: "Crop Water Stress",
        kpi_drought_risk: "Drought Risk", kpi_prediction: "Prediction",
        kpi_irrigation_req: "Irrigation required", kpi_low: "Low", kpi_mod: "Moderate", kpi_high: "High",
        dash_live_weather: "Live Weather", dash_forecast: "7-Day Forecast",
        // Weather
        status_api_connected: "Weather API Connected", ext_forecast: "Extended Forecast",
        // Predictor
        pred_title: "AI Yield & Irrigation Predictor", pred_live_inputs: "Live Weather Inputs",
        pred_autofill: "Auto-filled from live weather", pred_farm_info: "Farm & Crop Information",
        lbl_temp: "Temperature (°C)", lbl_rain: "Rainfall (mm)", lbl_hum: "Humidity (%)",
        lbl_soil_moisture: "Soil Moisture (%)", lbl_crop: "Crop Type", lbl_soil: "Soil Type",
        lbl_size: "Field Size (ha)", lbl_growth_stage: "Growth Stage", btn_predict: "Predict Yield & Irrigation",
        opt_cotton: "Cotton", opt_wheat: "Wheat", opt_tomato: "Tomato", opt_potato: "Potato",
        opt_sandy: "Sandy", opt_loamy: "Loamy", opt_clay: "Clay",
        res_title: "Prediction Result", res_risk: "Risk Score:", res_water: "Water Required:",
        res_reasoning: "AI Reasoning", res_yield: "Yield Prediction:",
        badge_irrigate: "IRRIGATE", badge_no_irrigate: "DO NOT IRRIGATE",
        data_source_live: "LIVE", data_source_cache: "CACHE", data_source_fallback: "DEMO",
        data_source_estimated: "ESTIMATED", data_source_sensor: "SENSOR", data_source_manual: "MANUAL",
        // Risk
        risk_overall: "Overall Risk Score", risk_factors: "Risk Factors",
        risk_drought: "Drought Risk", risk_heat: "Heat Stress",
        risk_water: "Water Stress", risk_flood: "Flood Risk",
        risk_high: "HIGH RISK", risk_moderate: "MODERATE RISK", risk_low: "LOW RISK",
        // Water
        water_title: "Water Management & Irrigation Planner",
        water_rec: "Recommended Irrigation — Next 7 Days",
        water_total: "Total Water Need", water_avg: "Average Per Day", water_forecast: "Forecast Rainfall",
        // Analytics
        hist_title: "Prediction History",
        th_date: "Date", th_crop: "Crop", th_moisture: "Moisture", th_rec: "Recommendation", th_risk: "Risk",
        hist_irrigate: "Irrigate", hist_wait: "Wait",
        // Field
        field_info: "Field Information", field_id: "Field ID", field_area: "Area",
        field_crop: "Crop", field_soil: "Soil Type", field_stage: "Growth Stage",
        field_moisture: "Latest Soil Moisture", field_veg: "Vegetative",
        // Alerts
        alert_heat_title: "High temperature expected",
        alert_heat_desc: "Monitor crop water requirements carefully over the next 48 hours.",
        alert_rain_title: "Low rainfall expected",
        alert_rain_desc: "Consider adjusting irrigation planning.",
        alert_sys_title: "System operating normally",
        alert_sys_desc: "All sensors and data streams are active.",
        // Reports
        rep_total: "Total Reports", rep_this_month: "This month",
        rep_water_saved: "Water Saved", rep_vs_manual: "vs manual irrigation",
        rep_predictions_made: "Predictions Made", rep_all_time: "All time",
        rep_generate: "Generate Report",
        rep_desc: "Download comprehensive insights on water usage, crop yield, and historical weather patterns for auditing and compliance.",
        rep_type: "Report Type", rep_period: "Period", rep_format: "Format",
        rep_opt_water: "Water Consumption Report", rep_opt_yield: "Yield Prediction Summary",
        rep_opt_risk: "Risk & Climate Audit", rep_opt_irr: "Irrigation History",
        rep_opt_full: "Full Platform Report",
        rep_opt_last_week: "Last 7 Days", rep_opt_last_month: "Last 30 Days",
        rep_opt_quarter: "Last Quarter", rep_opt_season: "Current Season",
        rep_btn_dl: "Download Report", rep_recent: "Recent Reports",
        rep_status: "Status", rep_ready: "Ready",
        // Settings
        set_general: "General Settings", set_default_loc: "Default Location",
        set_refresh: "Data Refresh Interval",
        set_5min: "Every 5 Minutes", set_15min: "Every 15 Minutes",
        set_30min: "Every 30 Minutes", set_1hr: "Every Hour",
        set_units: "Measurement Units",
        set_metric: "Metric (Celsius, mm, Hectares)", set_imperial: "Imperial (Fahrenheit, inches, Acres)",
        set_lang: "Interface Language",
        set_notif_settings: "Notification Settings", set_notif: "Alert Level",
        set_all: "All Alerts", set_critical: "Critical Only", set_none: "None",
        set_drought_thresh: "Drought Risk Threshold",
        set_data: "Data & API", set_api_key: "Custom API Key (Optional)",
        set_cache: "Cache Duration (min)",
        set_data_note_title: "Data Storage",
        set_data_note: "Prediction history and weather caches are stored locally in the SQLite database. No data is sent to third-party analytics services.",
        set_save: "Save Preferences",
        // Help
        help_about_platform: "About SWIP",
        help_about_text: "SWIP (Smart Water & Irrigation Platform) is an AI-powered agricultural decision support system designed specifically for Tajikistan. It combines real-time weather data from Open-Meteo with machine learning models to provide irrigation recommendations, risk assessments, and water management insights. The platform supports Cotton, Wheat, Tomato, and Potato crops across all regions including Dushanbe, Sughd, Khatlon, Badakhshan, and the Districts of Republican Subordination.",
        help_faq: "Frequently Asked Questions",
        help_q1: "How is the Irrigation Recommendation calculated?",
        help_a1: "It uses the difference between Evapotranspiration (ET₀) and Rainfall, scaled by your field size and crop-specific water coefficients. The ML model also factors in temperature, humidity, and soil moisture.",
        help_q2: "Where does the weather data come from?",
        help_a2: "Weather data is fetched in real-time from the Open-Meteo API, which provides free, non-commercial access to global weather forecasts. Coordinates are pre-configured for all major Tajik regions.",
        help_q3: "What does the Risk Score mean?",
        help_a3: "The Risk Score (0–100) combines drought risk (based on rainfall), heat stress (based on temperature), and water stress (based on soil moisture). A score below 35 is Low, 35–70 is Moderate, and above 70 is High risk.",
        help_q4: "Can I add a new location?",
        help_a4: "Currently locations are pre-configured by the system administrator. Contact the platform team to request additional locations with their GPS coordinates.",
        help_q5: "What is ET₀ (Evapotranspiration)?",
        help_a5: "ET₀ measures how much water evaporates from soil and transpires from plants per day (mm/day). It is calculated using the FAO Penman-Monteith method and is a key input for irrigation planning.",
        help_q6: "How often is the weather data refreshed?",
        help_a6: "Weather data is cached for 30 minutes by default. You can manually refresh using the ↻ button in the top bar, or change the refresh interval in Settings.",
        help_support: "Contact & Support", help_email: "Email Support", help_phone: "Phone",
        help_version: "SWIP v2.0 — Smart Water & Irrigation Platform for Tajikistan"
    },
    ru: {
        nav_subtitle: "Умная водная и\nирригационная платформа",
        nav_dashboard: "Панель", nav_weather: "Погода", nav_predictor: "Прогноз",
        nav_risk: "Оценка рисков", nav_water: "Управление водой", nav_field: "Поле и почва",
        nav_analytics: "Аналитика", nav_alerts: "Оповещения", nav_reports: "Отчёты",
        nav_settings: "Настройки", nav_help: "Помощь",
        last_updated: "Обновлено: --",
        dash_welcome: "Добро пожаловать, Agri Guard",
        dash_desc: "Текущее состояние ваших полей на основе данных погоды в реальном времени.",
        kpi_water_need: "Потребность в воде", kpi_water_stress: "Водный стресс",
        kpi_drought_risk: "Риск засухи", kpi_prediction: "Прогноз",
        kpi_irrigation_req: "Требуется полив", kpi_low: "Низкий", kpi_mod: "Умеренный", kpi_high: "Высокий",
        dash_live_weather: "Погода сейчас", dash_forecast: "Прогноз на 7 дней",
        status_api_connected: "API погоды подключён", ext_forecast: "Расширенный прогноз",
        pred_title: "ИИ-прогноз урожая и полива", pred_live_inputs: "Данные погоды",
        pred_autofill: "Автозаполнено из погоды", pred_farm_info: "Информация о поле",
        lbl_temp: "Температура (°C)", lbl_rain: "Осадки (мм)", lbl_hum: "Влажность (%)",
        lbl_soil_moisture: "Влажность почвы (%)", lbl_crop: "Тип культуры", lbl_soil: "Тип почвы",
        lbl_size: "Площадь поля (га)", lbl_growth_stage: "Стадия роста", btn_predict: "Прогнозировать",
        opt_cotton: "Хлопок", opt_wheat: "Пшеница", opt_tomato: "Томат", opt_potato: "Картофель",
        opt_sandy: "Песчаная", opt_loamy: "Суглинистая", opt_clay: "Глинистая",
        res_title: "Результат прогноза", res_risk: "Уровень риска:", res_water: "Требуется воды:",
        res_reasoning: "Объяснение ИИ", res_yield: "Прогноз урожая:",
        badge_irrigate: "ПОЛИВАТЬ", badge_no_irrigate: "НЕ ПОЛИВАТЬ",
        data_source_live: "LIVE", data_source_cache: "КЕШ", data_source_fallback: "ДЕМО",
        data_source_estimated: "ОЦЕНКА", data_source_sensor: "ДАТЧИК", data_source_manual: "ВВОД",
        risk_overall: "Общий балл риска", risk_factors: "Факторы риска",
        risk_drought: "Риск засухи", risk_heat: "Тепловой стресс",
        risk_water: "Водный стресс", risk_flood: "Риск наводнения",
        risk_high: "ВЫСОКИЙ РИСК", risk_moderate: "УМЕРЕННЫЙ РИСК", risk_low: "НИЗКИЙ РИСК",
        water_title: "Управление водой и планирование полива",
        water_rec: "Рекомендуемый полив — 7 дней",
        water_total: "Общая потребность", water_avg: "Среднее в день", water_forecast: "Прогноз осадков",
        hist_title: "История прогнозов",
        th_date: "Дата", th_crop: "Культура", th_moisture: "Влажность", th_rec: "Рекомендация", th_risk: "Риск",
        hist_irrigate: "Поливать", hist_wait: "Подождать",
        field_info: "Информация о поле", field_id: "ID поля", field_area: "Площадь",
        field_crop: "Культура", field_soil: "Тип почвы", field_stage: "Стадия роста",
        field_moisture: "Влажность почвы", field_veg: "Вегетативная",
        alert_heat_title: "Ожидается высокая температура",
        alert_heat_desc: "Следите за потребностью в воде в ближайшие 48 часов.",
        alert_rain_title: "Ожидается мало осадков",
        alert_rain_desc: "Рассмотрите корректировку плана полива.",
        alert_sys_title: "Система работает нормально",
        alert_sys_desc: "Все датчики и потоки данных активны.",
        rep_total: "Всего отчётов", rep_this_month: "В этом месяце",
        rep_water_saved: "Сэкономлено воды", rep_vs_manual: "по сравнению с ручным поливом",
        rep_predictions_made: "Всего прогнозов", rep_all_time: "За всё время",
        rep_generate: "Создать отчёт",
        rep_desc: "Скачайте подробную информацию об использовании воды, урожайности и погодных данных для аудита.",
        rep_type: "Тип отчёта", rep_period: "Период", rep_format: "Формат",
        rep_opt_water: "Отчёт о потреблении воды", rep_opt_yield: "Сводка прогнозов урожая",
        rep_opt_risk: "Аудит рисков и климата", rep_opt_irr: "История полива",
        rep_opt_full: "Полный отчёт платформы",
        rep_opt_last_week: "Последние 7 дней", rep_opt_last_month: "Последние 30 дней",
        rep_opt_quarter: "Последний квартал", rep_opt_season: "Текущий сезон",
        rep_btn_dl: "Скачать отчёт", rep_recent: "Последние отчёты",
        rep_status: "Статус", rep_ready: "Готов",
        set_general: "Общие настройки", set_default_loc: "Локация по умолчанию",
        set_refresh: "Интервал обновления",
        set_5min: "Каждые 5 минут", set_15min: "Каждые 15 минут",
        set_30min: "Каждые 30 минут", set_1hr: "Каждый час",
        set_units: "Единицы измерения",
        set_metric: "Метрическая (°C, мм, Гектары)", set_imperial: "Имперская (°F, дюймы, Акры)",
        set_lang: "Язык интерфейса",
        set_notif_settings: "Настройки уведомлений", set_notif: "Уровень оповещений",
        set_all: "Все оповещения", set_critical: "Только критические", set_none: "Нет",
        set_drought_thresh: "Порог риска засухи",
        set_data: "Данные и API", set_api_key: "API-ключ (необязательно)",
        set_cache: "Время кеша (мин)",
        set_data_note_title: "Хранение данных",
        set_data_note: "История прогнозов и кеш погоды хранятся локально в базе данных SQLite. Никакие данные не передаются сторонним аналитическим сервисам.",
        set_save: "Сохранить настройки",
        help_about_platform: "О платформе SWIP",
        help_about_text: "SWIP — ИИ-платформа поддержки сельскохозяйственных решений для Таджикистана. Она объединяет данные погоды от Open-Meteo с моделями машинного обучения для предоставления рекомендаций по поливу, оценки рисков и управления водными ресурсами. Платформа поддерживает хлопок, пшеницу, томаты и картофель во всех регионах.",
        help_faq: "Часто задаваемые вопросы",
        help_q1: "Как рассчитывается рекомендация по поливу?",
        help_a1: "Используется разница между эвапотранспирацией (ET₀) и осадками с учётом площади поля и коэффициентов культур. ML-модель также учитывает температуру, влажность и влажность почвы.",
        help_q2: "Откуда берутся данные о погоде?",
        help_a2: "Данные погоды получаются в реальном времени от API Open-Meteo. Координаты предварительно настроены для всех крупных регионов Таджикистана.",
        help_q3: "Что означает балл риска?",
        help_a3: "Балл риска (0–100) объединяет засуху, тепловой стресс и водный стресс. Менее 35 — низкий, 35–70 — умеренный, выше 70 — высокий риск.",
        help_q4: "Можно ли добавить новую локацию?",
        help_a4: "Локации настраиваются администратором. Обратитесь к команде платформы с GPS-координатами.",
        help_q5: "Что такое ET₀ (эвапотранспирация)?",
        help_a5: "ET₀ измеряет количество воды, испаряющейся из почвы и растений за день (мм/день). Это ключевой параметр для планирования полива.",
        help_q6: "Как часто обновляются данные погоды?",
        help_a6: "Данные погоды кешируются на 30 минут. Обновите вручную кнопкой ↻ или измените интервал в Настройках.",
        help_support: "Контакты и поддержка", help_email: "Поддержка по email", help_phone: "Телефон",
        help_version: "SWIP v2.0 — Умная водная и ирригационная платформа для Таджикистана"
    },
    tg: {
        nav_subtitle: "Платформаи зеҳнии об ва\nобёрӣ",
        nav_dashboard: "Панел", nav_weather: "Обу ҳаво", nav_predictor: "Пешгӯикунанда",
        nav_risk: "Баҳодиҳии хавф", nav_water: "Идоракунии об", nav_field: "Замин ва хок",
        nav_analytics: "Таҳлил", nav_alerts: "Огоҳиҳо", nav_reports: "Ҳисоботҳо",
        nav_settings: "Танзимот", nav_help: "Кумак",
        last_updated: "Навсозӣ: --",
        dash_welcome: "Хуш омадед, Agri Guard",
        dash_desc: "Ҳолати кунунии майдонҳои шумо дар асоси маълумоти обу ҳаво.",
        kpi_water_need: "Талаботи оби имрӯз", kpi_water_stress: "Стресси обӣ",
        kpi_drought_risk: "Хатари хушксолӣ", kpi_prediction: "Пешгӯӣ",
        kpi_irrigation_req: "Обёрӣ лозим аст", kpi_low: "Паст", kpi_mod: "Мӯътадил", kpi_high: "Баланд",
        dash_live_weather: "Обу ҳавои ҳозира", dash_forecast: "Пешгӯии 7-рӯза",
        status_api_connected: "API обу ҳаво пайваст аст", ext_forecast: "Пешгӯии васеъ",
        pred_title: "Пешгӯии ҳосил ва обёрӣ бо ИИ", pred_live_inputs: "Маълумоти обу ҳаво",
        pred_autofill: "Аз обу ҳавои зинда пур шуд", pred_farm_info: "Маълумоти хоҷагӣ",
        lbl_temp: "Ҳарорат (°C)", lbl_rain: "Боришот (мм)", lbl_hum: "Намнокӣ (%)",
        lbl_soil_moisture: "Намнокии хок (%)", lbl_crop: "Намуди зироат", lbl_soil: "Намуди хок",
        lbl_size: "Масоҳат (га)", lbl_growth_stage: "Марҳилаи рушд", btn_predict: "Пешгӯӣ кунед",
        opt_cotton: "Пахта", opt_wheat: "Гандум", opt_tomato: "Помидор", opt_potato: "Картошка",
        opt_sandy: "Регӣ", opt_loamy: "Хокдор", opt_clay: "Гилӣ",
        res_title: "Натиҷаи пешгӯӣ", res_risk: "Дараҷаи хавф:", res_water: "Оби лозим:",
        res_reasoning: "Шарҳи ИИ", res_yield: "Пешгӯии ҳосил:",
        badge_irrigate: "ОБЁРӢ КУНЕД", badge_no_irrigate: "ОБЁРӢ НАКУНЕД",
        data_source_live: "ЗИНДА", data_source_cache: "КЕШ", data_source_fallback: "ДЕМО",
        data_source_estimated: "ТАХМИНӢ", data_source_sensor: "ДАТЧИК", data_source_manual: "ДАСТӢ",
        risk_overall: "Баҳои умумии хавф", risk_factors: "Омилҳои хавф",
        risk_drought: "Хатари хушксолӣ", risk_heat: "Стресси гармӣ",
        risk_water: "Стресси обӣ", risk_flood: "Хатари обхезӣ",
        risk_high: "ХАВФИ БАЛАНД", risk_moderate: "ХАВФИ МӮЪТАДИЛ", risk_low: "ХАВФИ ПАСТ",
        water_title: "Идоракунии об ва нақшаи обёрӣ",
        water_rec: "Обёрии тавсияшуда — 7 рӯз",
        water_total: "Ҳаҷми умумӣ", water_avg: "Миёна дар рӯз", water_forecast: "Пешгӯии боришот",
        hist_title: "Таърихи пешгӯиҳо",
        th_date: "Сана", th_crop: "Зироат", th_moisture: "Намнокӣ", th_rec: "Тавсия", th_risk: "Хавф",
        hist_irrigate: "Обёрӣ кунед", hist_wait: "Интизор шавед",
        field_info: "Маълумоти замин", field_id: "ID замин", field_area: "Масоҳат",
        field_crop: "Зироат", field_soil: "Намуди хок", field_stage: "Марҳилаи рушд",
        field_moisture: "Намнокии хок", field_veg: "Вегетативӣ",
        alert_heat_title: "Ҳарорати баланд интизор аст",
        alert_heat_desc: "Талаботи обро дар 48 соати оянда назорат кунед.",
        alert_rain_title: "Боришоти кам интизор аст",
        alert_rain_desc: "Нақшаи обёриро танзим кунед.",
        alert_sys_title: "Система нормал кор мекунад",
        alert_sys_desc: "Ҳамаи датчикҳо ва маълумот фаъоланд.",
        rep_total: "Ҳисоботҳои умумӣ", rep_this_month: "Ин моҳ",
        rep_water_saved: "Оби сарфашуда", rep_vs_manual: "назар ба обёрии дастӣ",
        rep_predictions_made: "Пешгӯиҳои иҷрошуда", rep_all_time: "Тамоми вақт",
        rep_generate: "Сохтани ҳисобот",
        rep_desc: "Маълумоти муфассал дар бораи истифодаи об, ҳосилнокӣ ва обу ҳаворо зеркашӣ кунед.",
        rep_type: "Намуди ҳисобот", rep_period: "Давра", rep_format: "Формат",
        rep_opt_water: "Ҳисоботи истеъмоли об", rep_opt_yield: "Хулосаи пешгӯии ҳосил",
        rep_opt_risk: "Аудити хавф ва иқлим", rep_opt_irr: "Таърихи обёрӣ",
        rep_opt_full: "Ҳисоботи пурраи платформа",
        rep_opt_last_week: "7 рӯзи охир", rep_opt_last_month: "30 рӯзи охир",
        rep_opt_quarter: "Семоҳаи охир", rep_opt_season: "Мавсими ҷорӣ",
        rep_btn_dl: "Зеркашии ҳисобот", rep_recent: "Ҳисоботҳои охирин",
        rep_status: "Ҳолат", rep_ready: "Омода",
        set_general: "Танзимоти умумӣ", set_default_loc: "Ҷойгиршавии пешфарз",
        set_refresh: "Давраи навсозӣ",
        set_5min: "Ҳар 5 дақиқа", set_15min: "Ҳар 15 дақиқа",
        set_30min: "Ҳар 30 дақиқа", set_1hr: "Ҳар соат",
        set_units: "Воҳидҳои ченак",
        set_metric: "Метрикӣ (°C, мм, Гектар)", set_imperial: "Империалӣ (°F, дюйм, Акр)",
        set_lang: "Забони интерфейс",
        set_notif_settings: "Танзимоти огоҳиҳо", set_notif: "Сатҳи огоҳӣ",
        set_all: "Ҳамаи огоҳиҳо", set_critical: "Танҳо муҳим", set_none: "Ҳеҷ",
        set_drought_thresh: "Ҳадди хатари хушксолӣ",
        set_data: "Маълумот ва API", set_api_key: "Калиди API (ихтиёрӣ)",
        set_cache: "Давраи кеш (дақиқа)",
        set_data_note_title: "Нигоҳдории маълумот",
        set_data_note: "Таърихи пешгӯиҳо ва кеши обу ҳаво дар базаи маълумоти SQLite нигоҳ дошта мешавад.",
        set_save: "Нигоҳ доштани танзимот",
        help_about_platform: "Дар бораи SWIP",
        help_about_text: "SWIP — системаи зеҳнии дастгирии қарор барои кишоварзии Тоҷикистон. Он маълумоти обу ҳаворо аз Open-Meteo бо моделҳои ИИ муттаҳид мекунад.",
        help_faq: "Саволҳои зуд-зуд пурсидашаванда",
        help_q1: "Тавсияи обёрӣ чӣ тавр ҳисоб мешавад?",
        help_a1: "Тафовути байни эвапотранспиратсия (ET₀) ва боришот бо назардошти масоҳати замин ва коэффисиентҳои зироатҳо.",
        help_q2: "Маълумоти обу ҳаво аз куҷо меояд?",
        help_a2: "Маълумоти обу ҳаво аз API Open-Meteo дар вақти воқеӣ гирифта мешавад.",
        help_q3: "Баҳои хавф чӣ маънӣ дорад?",
        help_a3: "Баҳои хавф (0–100) хушксолӣ, стресси гармӣ ва обиро муттаҳид мекунад. Зери 35 — паст, 35–70 — мӯътадил, болои 70 — баланд.",
        help_q4: "Оё ман метавонам ҷойгиршавии нав илова кунам?",
        help_a4: "Ҷойгиршавиҳо аз тарафи администратор танзим мешаванд. Бо координатаҳои GPS муроҷиат кунед.",
        help_q5: "ET₀ (эвапотранспиратсия) чист?",
        help_a5: "ET₀ миқдори обро, ки аз хок ва растаниҳо дар як рӯз буғ мешавад, чен мекунад (мм/рӯз).",
        help_q6: "Маълумоти обу ҳаво чанд вақт як бор навсозӣ мешавад?",
        help_a6: "Маълумоти обу ҳаво 30 дақиқа кеш мешавад. Бо тугмаи ↻ навсозӣ кунед ё давраро дар Танзимот иваз кунед.",
        help_support: "Тамос ва дастгирӣ", help_email: "Дастгирӣ тавассути email", help_phone: "Телефон",
        help_version: "SWIP v2.0 — Платформаи зеҳнии об ва обёрӣ барои Тоҷикистон"
    }
};

// ========== GLOBAL STATE ==========
let globalState = {
    location: null,
    weatherData: null,
    lastDecision: null, // Stores the last /api/decision response
    locationsList: [],
    lang: 'en'
};

// ========== UTILITY ==========
function clampNonNeg(val) {
    return Math.max(0, val);
}

function getDataSourceLabel(source) {
    const dict = T[globalState.lang] || T.en;
    const map = {
        'live': dict.data_source_live,
        'cache': dict.data_source_cache,
        'fallback': dict.data_source_fallback,
        'Estimated from weather models': dict.data_source_estimated,
        'Sensor measured': dict.data_source_sensor,
        'User entered': dict.data_source_manual
    };
    return map[source] || source;
}

function getDataSourceClass(source) {
    if (source === 'live' || source === 'Sensor measured') return 'data-source-live';
    if (source === 'cache' || source === 'User entered') return 'data-source-cache';
    return 'data-source-fallback';
}

// ========== i18n ENGINE ==========
function applyTranslations(lang) {
    globalState.lang = lang;
    const dict = T[lang] || T.en;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key] !== undefined) {
            // Preserve icons inside nav links
            const icon = el.querySelector('i[data-lucide]');
            if (icon) {
                const iconName = icon.getAttribute('data-lucide');
                const iconClass = icon.getAttribute('class') || '';
                el.innerHTML = `<i data-lucide="${iconName}" class="${iconClass}"></i>${dict[key]}`;
            } else {
                el.textContent = dict[key];
            }
        }
    });
    // Re-render lucide icons after DOM changes
    if (typeof lucide !== 'undefined') { lucide.createIcons(); }
}

// ========== INIT ==========
document.addEventListener('DOMContentLoaded', async () => {
    if (typeof lucide !== 'undefined') { lucide.createIcons(); }

    setupNavigation();
    setupLanguageSwitcher();
    updateDate();

    await fetchLocations();

    const locationSelect = document.getElementById('location-select');
    locationSelect.addEventListener('change', async (e) => {
        await fetchWeather(e.target.value);
        updateBackground(e.target.value);
    });

    document.getElementById('refresh-btn').addEventListener('click', async () => {
        if (locationSelect.value) {
            await fetchWeather(locationSelect.value);
        }
    });

    setupPredictionForm();
    setupReportDownload();
    loadHistory();
});

// ========== LANGUAGE SWITCHER ==========
function setupLanguageSwitcher() {
    const topbarLang = document.getElementById('lang-select');
    const settingsLang = document.getElementById('settings-lang-select');

    topbarLang.addEventListener('change', (e) => {
        applyTranslations(e.target.value);
        if (settingsLang) settingsLang.value = e.target.value;
        // Re-render dynamic content that was generated by JS
        if (globalState.weatherData) updateDashboardWithWeather(globalState.weatherData);
        loadHistory();
    });

    if (settingsLang) {
        settingsLang.addEventListener('change', (e) => {
            applyTranslations(e.target.value);
            topbarLang.value = e.target.value;
            if (globalState.weatherData) updateDashboardWithWeather(globalState.weatherData);
            loadHistory();
        });
    }
}

// ========== NAVIGATION ==========
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-links li');
    const sections = document.querySelectorAll('.page-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const targetId = link.getAttribute('data-target');
            sections.forEach(sec => sec.classList.remove('active'));
            document.getElementById(targetId).classList.add('active');

            if (targetId === 'analytics') loadHistory();
            if (targetId === 'water' && window.updateIrrigationChart) {
                window.updateIrrigationChart(globalState.weatherData);
            }
            // Re-render lucide icons inside newly visible sections
            if (typeof lucide !== 'undefined') { lucide.createIcons(); }
        });
    });
}

function updateDate() {
    const now = new Date();
    const lang = globalState.lang;
    const dict = T[lang] || T.en;
    const prefix = dict.last_updated.split(':')[0] + ':';
    document.getElementById('last-updated').innerText = `${prefix} ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
}

function updateBackground(locationId) {
    const bgLayer = document.getElementById('bg-layer');
    const images = {
        'dushanbe': 'pamir_mountain.jpg',
        'khujand': 'agricultural_hills.jpg',
        'sughd': 'agricultural_hills.jpg',
        'bokhtar': 'cotton_plantation.jpg',
        'khatlon': 'cotton_plantation.jpg',
        'khorugh': 'reservoir_lake.jpg',
        'badakhshan': 'reservoir_lake.jpg',
        'drs': 'agricultural_hills.jpg'
    };
    const imgName = images[locationId] || 'pamir_mountain.jpg';
    bgLayer.style.backgroundImage = `url('/static/images/${imgName}')`;
}

// ========== DATA FETCHING ==========
async function fetchLocations() {
    try {
        const res = await fetch('/api/locations');
        const data = await res.json();
        globalState.locationsList = data;

        const select = document.getElementById('location-select');
        const settingsSelect = document.getElementById('settings-default-loc');
        select.innerHTML = '';
        if (settingsSelect) settingsSelect.innerHTML = '';

        data.forEach(loc => {
            const opt = document.createElement('option');
            opt.value = loc.id;
            opt.innerText = loc.name;
            select.appendChild(opt);

            if (settingsSelect) {
                const opt2 = opt.cloneNode(true);
                settingsSelect.appendChild(opt2);
            }
        });

        if (data.length > 0) {
            select.value = data[0].id;
            await fetchWeather(data[0].id);
            updateBackground(data[0].id);
        }
    } catch (e) {
        console.error("Error fetching locations:", e);
    }
}

async function fetchWeather(locationId) {
    try {
        const res = await fetch(`/api/weather?location=${locationId}`);
        const data = await res.json();
        globalState.weatherData = data;

        updateDashboardWithWeather(data);
        autoFillPredictor(data);
        updateDate();

        // Update weather data source badge
        updateWeatherSourceBadge(data.data_source || 'live');

        if (window.updateIrrigationChart) {
            window.updateIrrigationChart(data);
        }
    } catch (e) {
        console.error("Error fetching weather:", e);
    }
}

function updateWeatherSourceBadge(source) {
    const badge = document.getElementById('weather-source-badge');
    if (badge) {
        badge.innerText = getDataSourceLabel(source);
        badge.className = `data-source-badge ${getDataSourceClass(source)}`;
    }
}

// ========== DASHBOARD ==========
// NOTE: Dashboard KPIs are now display-only from weather data.
// Authoritative risk/yield/water calculations come ONLY from /api/decision.
function updateDashboardWithWeather(data) {
    if (!data) return;
    const c = data.current;
    const lang = globalState.lang;
    const dict = T[lang] || T.en;

    // Temperature can be negative, everything else is clamped to >= 0
    document.getElementById('dash-temp').innerText = `${Math.round(c.temperature)}°C`;
    document.getElementById('dash-rain').innerText = `${clampNonNeg(c.rainfall).toFixed(1)} mm`;
    document.getElementById('dash-humidity').innerText = `${clampNonNeg(Math.round(c.humidity))}%`;
    document.getElementById('dash-wind').innerText = `${clampNonNeg(c.wind_speed).toFixed(1)} km/h`;
    document.getElementById('dash-et0').innerText = `${clampNonNeg(data.et0).toFixed(1)} mm/d`;

    // KPI: Water Need (from ET0 — display only, not authoritative)
    const waterNeed = clampNonNeg(data.et0 * 2);
    document.getElementById('dash-water-need').innerText = `${waterNeed.toFixed(1)} mm`;

    // KPI: Drought Risk and Water Stress — show "—" until a real decision is made
    const dashDrought = document.getElementById('dash-drought-risk');
    const dashStress = document.getElementById('dash-water-stress');
    const dashYield = document.getElementById('dash-yield');

    if (globalState.lastDecision) {
        // Use real backend data
        const risk = globalState.lastDecision.risk;
        dashDrought.innerText = `${risk.drought}/100`;
        const lvlEl = document.getElementById('dash-drought-lvl');
        if (risk.drought > 70) { lvlEl.innerText = dict.kpi_high; lvlEl.className = "kpi-subtext text-danger"; }
        else if (risk.drought > 35) { lvlEl.innerText = dict.kpi_mod; lvlEl.className = "kpi-subtext text-warning"; }
        else { lvlEl.innerText = dict.kpi_low; lvlEl.className = "kpi-subtext text-success"; }

        dashStress.innerText = `${risk.water_stress}%`;
        const stressLvlEl = document.getElementById('dash-stress-lvl');
        if (risk.water_stress > 50) { stressLvlEl.innerText = dict.kpi_high; stressLvlEl.className = "kpi-subtext text-danger"; }
        else if (risk.water_stress > 20) { stressLvlEl.innerText = dict.kpi_mod; stressLvlEl.className = "kpi-subtext text-warning"; }
        else { stressLvlEl.innerText = dict.kpi_low; stressLvlEl.className = "kpi-subtext text-success"; }

        dashYield.innerText = `${globalState.lastDecision.yield.prediction_t_ha} t/ha`;

        // Risk scorer page — use backend data
        document.getElementById('risk-overall-score').innerText = risk.overall;
        const riskLevelEl = document.getElementById('risk-overall-level');
        if (risk.level === 'HIGH') { riskLevelEl.innerText = dict.risk_high; riskLevelEl.className = 'risk-level-text text-danger'; }
        else if (risk.level === 'MEDIUM') { riskLevelEl.innerText = dict.risk_moderate; riskLevelEl.className = 'risk-level-text text-warning'; }
        else { riskLevelEl.innerText = dict.risk_low; riskLevelEl.className = 'risk-level-text text-success'; }

        // Risk factor bars
        updateRiskBar('drought-bar', risk.drought);
        updateRiskBar('heat-bar', risk.heat);
        updateRiskBar('water-bar', risk.water_stress);
        updateRiskBar('flood-bar', risk.flood);
    } else {
        dashDrought.innerText = '—';
        dashStress.innerText = '—';
        dashYield.innerText = '—';
    }

    // Forecast List
    const forecastList = document.getElementById('dash-forecast');
    forecastList.innerHTML = '';
    data.forecast.slice(0, 7).forEach(day => {
        const d = new Date(day.date + 'T00:00:00').toLocaleDateString(lang === 'ru' ? 'ru-RU' : (lang === 'tg' ? 'tg-TJ' : 'en-US'), { weekday: 'short', month: 'short', day: 'numeric' });
        const el = document.createElement('div');
        el.className = 'forecast-item';
        el.innerHTML = `
            <span>${d}</span>
            <span>${clampNonNeg(Math.round(day.precip_prob))}%</span>
            <span>${Math.round(day.max_temp)}° / ${Math.round(day.min_temp)}°</span>
        `;
        forecastList.appendChild(el);
    });

    // Water planner - forecast rainfall
    const totalRain = clampNonNeg(data.forecast.reduce((a, b) => a + clampNonNeg(b.precipitation), 0));
    document.getElementById('water-forecast-rain').innerText = `${totalRain.toFixed(1)} mm`;

    // Reports page prediction count
    const repCount = document.getElementById('rep-pred-count');
    if (repCount) repCount.innerText = '--'; // Will be updated after history loads

    if (typeof lucide !== 'undefined') { lucide.createIcons(); }
}

function updateRiskBar(elementId, value) {
    const bar = document.getElementById(elementId);
    if (bar) {
        bar.style.width = `${Math.min(100, Math.max(0, value))}%`;
        if (value > 70) bar.style.backgroundColor = '#ef4444';
        else if (value > 35) bar.style.backgroundColor = '#f59e0b';
        else bar.style.backgroundColor = '#22c55e';
    }
}

// ========== PREDICTOR ==========
function autoFillPredictor(data) {
    if (!data) return;
    document.getElementById('pred-temp').value = data.current.temperature;
    document.getElementById('pred-rain').value = clampNonNeg(data.current.rainfall);
    document.getElementById('pred-humidity').value = clampNonNeg(data.current.humidity);
    document.getElementById('pred-soil-moisture').value = clampNonNeg(Math.min(100, 20 + clampNonNeg(data.current.rainfall) * 5));
}

function setupPredictionForm() {
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clamp non-temperature values before sending
        const rainfall = Math.max(0, parseFloat(document.getElementById('pred-rain').value) || 0);
        const humidity = Math.max(0, parseFloat(document.getElementById('pred-humidity').value) || 0);
        const soilMoisture = Math.max(0, parseFloat(document.getElementById('pred-soil-moisture').value) || 0);
        const fieldSize = Math.max(0.1, parseFloat(document.getElementById('pred-size').value) || 0.1);

        const locationSelect = document.getElementById('location-select');
        const locationName = locationSelect.options[locationSelect.selectedIndex]?.text || 'Unknown';

        // Get growth stage from form (new field)
        const growthStageEl = document.getElementById('pred-growth-stage');
        const growthStage = growthStageEl ? growthStageEl.value : 'Mid-Season';

        const payload = {
            location: locationName,
            temperature: parseFloat(document.getElementById('pred-temp').value),
            rainfall: rainfall,
            humidity: humidity,
            soil_moisture: soilMoisture,
            soil_moisture_source: "manual",
            crop_type: document.getElementById('pred-crop').value,
            soil_type: document.getElementById('pred-soil').value,
            field_size: fieldSize,
            growth_stage: growthStage,
            language: globalState.lang
        };

        try {
            const res = await fetch('/api/decision', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await res.json();

            if (!res.ok) {
                console.error("Decision API error:", result);
                return;
            }

            // Store the decision globally so dashboard can use it
            globalState.lastDecision = result;
            showDecisionResult(result);

            // Refresh dashboard KPIs with real backend data
            if (globalState.weatherData) {
                updateDashboardWithWeather(globalState.weatherData);
            }
        } catch (e) {
            console.error("Decision error:", e);
        }
    });
}

function showDecisionResult(data) {
    const panel = document.getElementById('prediction-result');
    panel.style.display = 'block';
    const lang = globalState.lang;
    const dict = T[lang] || T.en;

    const isRecommended = data.irrigation.recommended;
    const badge = document.getElementById('res-badge');
    badge.innerText = isRecommended ? dict.badge_irrigate : dict.badge_no_irrigate;
    badge.className = `badge ${isRecommended ? 'irrigate' : 'do-not-irrigate'}`;

    // Risk
    document.getElementById('res-risk').innerText = `${data.risk.overall} (${data.risk.level})`;

    // Water
    document.getElementById('res-water').innerText = `${data.irrigation.water_liters.toLocaleString()} L (${data.irrigation.amount_mm} mm)`;

    // Yield — FROM BACKEND, no more Math.random()!
    const yieldEl = document.getElementById('res-yield-value');
    if (yieldEl) {
        yieldEl.innerText = `${data.yield.prediction_t_ha} t/ha (${data.yield.range.lower}–${data.yield.range.upper})`;
    }
    document.getElementById('dash-yield').innerText = `${data.yield.prediction_t_ha} t/ha`;

    // Soil source badge
    const soilSourceEl = document.getElementById('res-soil-source');
    if (soilSourceEl) {
        soilSourceEl.innerText = getDataSourceLabel(data.soil_status.source);
        soilSourceEl.className = `data-source-badge ${getDataSourceClass(data.soil_status.source)}`;
    }

    // Reasons
    const reasonsList = document.getElementById('res-reasons-list');
    reasonsList.innerHTML = '';
    data.explanations.forEach(r => {
        const li = document.createElement('li');
        li.innerText = r;
        reasonsList.appendChild(li);
    });

    // Confidence bar
    const confBar = document.getElementById('res-confidence-bar');
    if (confBar) {
        confBar.style.width = `${data.irrigation.probability_percent}%`;
        confBar.innerText = `${data.irrigation.probability_percent}%`;
    }

    // Alerts section — update dynamically from backend
    if (data.alerts) {
        updateAlertsFromBackend(data.alerts);
    }
}

function updateAlertsFromBackend(alerts) {
    const container = document.getElementById('alerts-list');
    if (!container) return;
    container.innerHTML = '';

    alerts.forEach(alert => {
        const typeClass = alert.type === 'danger' ? 'alert-danger' :
            alert.type === 'warning' ? 'alert-warning' :
                alert.type === 'info' ? 'alert-info' : 'alert-success';
        const iconName = alert.type === 'danger' ? 'alert-triangle' :
            alert.type === 'warning' ? 'alert-circle' :
                alert.type === 'info' ? 'info' : 'check-circle';

        const el = document.createElement('div');
        el.className = `alert-card ${typeClass}`;
        el.innerHTML = `
            <div class="alert-icon"><i data-lucide="${iconName}"></i></div>
            <div class="alert-content">
                <strong>${alert.title}</strong>
                <p>${alert.desc}</p>
            </div>
        `;
        container.appendChild(el);
    });

    if (typeof lucide !== 'undefined') { lucide.createIcons(); }
}

// ========== REPORT DOWNLOAD ==========
function setupReportDownload() {
    const dlBtn = document.getElementById('report-download-btn');
    if (dlBtn) {
        dlBtn.addEventListener('click', async () => {
            try {
                const res = await fetch('/api/report?format=csv&limit=100');
                if (!res.ok) throw new Error('Report download failed');
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'swip_report.csv';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            } catch (e) {
                console.error("Report download error:", e);
            }
        });
    }
}

// ========== HISTORY ==========
async function loadHistory() {
    try {
        const res = await fetch('/api/history');
        const data = await res.json();
        const lang = globalState.lang;
        const dict = T[lang] || T.en;

        const tbody = document.querySelector('#history-table tbody');
        tbody.innerHTML = '';

        data.history.forEach(row => {
            const tr = document.createElement('tr');
            const date = new Date(row.timestamp).toLocaleDateString();
            const predClass = row.prediction === 1 ? 'irrigate' : 'do-not-irrigate';
            const predText = row.prediction === 1 ? dict.hist_irrigate : dict.hist_wait;

            tr.innerHTML = `
                <td>${date}</td>
                <td>${row.crop_type}</td>
                <td>${clampNonNeg(row.soil_moisture).toFixed(1)}%</td>
                <td><span class="badge ${predClass}" style="padding: 4px 10px; font-size: 11px;">${predText}</span></td>
                <td>${Math.max(0, row.risk_score)}</td>
            `;
            tbody.appendChild(tr);
        });

        // Update report prediction count
        const repCount = document.getElementById('rep-pred-count');
        if (repCount) repCount.innerText = data.history.length;
    } catch (e) {
        console.error("History error:", e);
    }
}
