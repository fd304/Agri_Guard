// SWIP browser integration; calculations are authoritative only from the backend.

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
        dash_desc: "Weather forecasts and user-entered analysis — not monitored farm observations.",
        kpi_water_need: "Final daily irrigation depth", kpi_water_stress: "Water-deficit index",
        kpi_drought_risk: "Daily dryness index", kpi_prediction: "Synthetic-model yield estimate",
        kpi_irrigation_req: "Run analysis for a final decision", kpi_low: "Low", kpi_mod: "Moderate", kpi_high: "High",
        dash_live_weather: "Live Weather", dash_forecast: "7-Day Forecast",
        // Weather
        status_api_connected: "Weather API Connected", ext_forecast: "Extended Forecast",
        // Predictor
        pred_title: "AI Yield & Irrigation Predictor", pred_live_inputs: "Daily analysis inputs",
        pred_autofill: "Enter daily values or explicitly use available forecast inputs. Soil moisture is never auto-observed.", pred_farm_info: "Farm & Crop Information",
        lbl_temp: "Temperature (°C)", lbl_rain: "Daily rainfall (mm)", lbl_hum: "Humidity (%)",
        lbl_soil_moisture: "Soil Moisture (%)", lbl_crop: "Crop Type", lbl_soil: "Soil Type",
        lbl_size: "Field Size (ha)", lbl_growth_stage: "Growth Stage", btn_predict: "Predict Yield & Irrigation",
        opt_cotton: "Cotton", opt_wheat: "Wheat", opt_tomato: "Tomato", opt_potato: "Potato",
        opt_sandy: "Sandy", opt_loamy: "Loamy", opt_clay: "Clay",
        res_title: "Prediction Result", res_risk: "Risk Score:", res_water: "Water Required:",
        res_reasoning: "Decision explanation & limitations", res_yield: "Yield Prediction:",
        badge_irrigate: "IRRIGATE", badge_no_irrigate: "DO NOT IRRIGATE",
        data_source_live: "LIVE", data_source_cache: "CACHE", data_source_fallback: "UNAVAILABLE",
        data_source_estimated: "ESTIMATED", data_source_sensor: "SENSOR", data_source_manual: "MANUAL",
        // Risk
        risk_overall: "Overall Risk Score", risk_factors: "Risk Factors",
        risk_drought: "Drought Risk", risk_heat: "Heat Stress",
        risk_water: "Water Stress", risk_flood: "Flood Risk",
        risk_high: "HIGH RISK", risk_moderate: "MODERATE RISK", risk_low: "LOW RISK",
        // Water
        water_title: "Water Management & Irrigation Planner",
        water_rec: "Forecast water-balance scenario — not an irrigation instruction",
        water_total: "Net depth total", water_avg: "Net depth per day", water_forecast: "Forecast Rainfall",
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
        rep_predictions_made: "Predictions Made", rep_all_time: "Latest 100 records (including unverified legacy records)",
        rep_generate: "Generate Report",
        rep_desc: "Export persisted analysis records. Volumes are recommendations, not metered consumption or proven savings.",
        rep_type: "Report Type", rep_period: "Period", rep_format: "Format",
        rep_opt_water: "Water requirement estimates", rep_opt_yield: "Yield Prediction Summary",
        rep_opt_risk: "Heuristic risk history", rep_opt_irr: "Irrigation History",
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
        help_about_text: "SWIP — Smart Water Intelligence Platform is a Tajikistan-focused demonstration. Open-Meteo provides modelled weather; all ML training inputs and targets in this repository are synthetic. No observed farm outcomes or field validation are available.",
        help_faq: "Frequently Asked Questions",
        help_q1: "How is the Irrigation Recommendation calculated?",
        help_a1: "A synthetic-target model is combined with an approximate daily water balance and safety overrides (>80% moisture or >30 mm daily rain). These legacy assumptions are not locally validated. Raw model and final rule-based decisions are shown separately.",
        help_q2: "Where does the weather data come from?",
        help_a2: "Open-Meteo provides modelled current conditions and forecasts, not farm sensor readings. Unavailable data is reported honestly. Cache responses carry their age; expired responses may be displayed for up to two hours with a warning.",
        help_q3: "What does the Risk Score mean?",
        help_a3: "Heuristic 0–100 indices, not measured damage or calibrated probabilities. Overall <=35: low, >35 to 70: medium, >70: high. Water-deficit stress and waterlogging are separate.",
        help_q4: "Can I add a new location?",
        help_a4: "Currently locations are pre-configured by the system administrator. Contact the platform team to request additional locations with their GPS coordinates.",
        help_q5: "What is ET₀ (Evapotranspiration)?",
        help_a5: "Reference evapotranspiration is in mm/day. Open-Meteo daily FAO ET0 is used when explicitly filled. With no supplied ET0, analysis uses an uncalibrated temperature/humidity heuristic, not Penman-Monteith.",
        help_q6: "How often is the weather data refreshed?",
        help_a6: "The browser refresh interval controls requests. The server cache is fixed at 30 minutes; repeated refreshes may return the same timestamp. No API key is required.",
        help_support: "Contact & Support", help_email: "Email Support", help_phone: "Phone",
        help_version: "SWIP 2.1 — synthetic-data demonstration, not field-validated guidance"
    },
    ru: {
        nav_subtitle: "Умная водная и\nирригационная платформа",
        nav_dashboard: "Панель", nav_weather: "Погода", nav_predictor: "Прогноз",
        nav_risk: "Оценка рисков", nav_water: "Управление водой", nav_field: "Поле и почва",
        nav_analytics: "Аналитика", nav_alerts: "Оповещения", nav_reports: "Отчёты",
        nav_settings: "Настройки", nav_help: "Помощь",
        last_updated: "Обновлено: --",
        dash_welcome: "Добро пожаловать, Agri Guard",
        dash_desc: "Weather forecasts and user-entered analysis — not monitored farm observations.",
        kpi_water_need: "Final daily irrigation depth", kpi_water_stress: "Water-deficit index",
        kpi_drought_risk: "Daily dryness index", kpi_prediction: "Synthetic-model yield estimate",
        kpi_irrigation_req: "Run analysis for a final decision", kpi_low: "Низкий", kpi_mod: "Умеренный", kpi_high: "Высокий",
        dash_live_weather: "Погода сейчас", dash_forecast: "Прогноз на 7 дней",
        status_api_connected: "API погоды подключён", ext_forecast: "Расширенный прогноз",
        pred_title: "ИИ-прогноз урожая и полива", pred_live_inputs: "Daily analysis inputs",
        pred_autofill: "Enter daily values or explicitly use available forecast inputs. Soil moisture is never auto-observed.", pred_farm_info: "Информация о поле",
        lbl_temp: "Температура (°C)", lbl_rain: "Daily rainfall (mm)", lbl_hum: "Влажность (%)",
        lbl_soil_moisture: "Влажность почвы (%)", lbl_crop: "Тип культуры", lbl_soil: "Тип почвы",
        lbl_size: "Площадь поля (га)", lbl_growth_stage: "Стадия роста", btn_predict: "Прогнозировать",
        opt_cotton: "Хлопок", opt_wheat: "Пшеница", opt_tomato: "Томат", opt_potato: "Картофель",
        opt_sandy: "Песчаная", opt_loamy: "Суглинистая", opt_clay: "Глинистая",
        res_title: "Результат прогноза", res_risk: "Уровень риска:", res_water: "Требуется воды:",
        res_reasoning: "Decision explanation & limitations", res_yield: "Прогноз урожая:",
        badge_irrigate: "ПОЛИВАТЬ", badge_no_irrigate: "НЕ ПОЛИВАТЬ",
        data_source_live: "LIVE", data_source_cache: "КЕШ", data_source_fallback: "UNAVAILABLE",
        data_source_estimated: "ОЦЕНКА", data_source_sensor: "ДАТЧИК", data_source_manual: "ВВОД",
        risk_overall: "Общий балл риска", risk_factors: "Факторы риска",
        risk_drought: "Риск засухи", risk_heat: "Тепловой стресс",
        risk_water: "Водный стресс", risk_flood: "Риск наводнения",
        risk_high: "ВЫСОКИЙ РИСК", risk_moderate: "УМЕРЕННЫЙ РИСК", risk_low: "НИЗКИЙ РИСК",
        water_title: "Управление водой и планирование полива",
        water_rec: "Forecast water-balance scenario — not an irrigation instruction",
        water_total: "Net depth total", water_avg: "Net depth per day", water_forecast: "Прогноз осадков",
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
        rep_predictions_made: "Всего прогнозов", rep_all_time: "Latest 100 records (including unverified legacy records)",
        rep_generate: "Создать отчёт",
        rep_desc: "Export persisted analysis records. Volumes are recommendations, not metered consumption or proven savings.",
        rep_type: "Тип отчёта", rep_period: "Период", rep_format: "Формат",
        rep_opt_water: "Water requirement estimates", rep_opt_yield: "Сводка прогнозов урожая",
        rep_opt_risk: "Heuristic risk history", rep_opt_irr: "История полива",
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
        help_about_text: "SWIP — Smart Water Intelligence Platform is a Tajikistan-focused demonstration. Open-Meteo provides modelled weather; all ML training inputs and targets in this repository are synthetic. No observed farm outcomes or field validation are available.",
        help_faq: "Часто задаваемые вопросы",
        help_q1: "Как рассчитывается рекомендация по поливу?",
        help_a1: "A synthetic-target model is combined with an approximate daily water balance and safety overrides (>80% moisture or >30 mm daily rain). These legacy assumptions are not locally validated. Raw model and final rule-based decisions are shown separately.",
        help_q2: "Откуда берутся данные о погоде?",
        help_a2: "Open-Meteo provides modelled current conditions and forecasts, not farm sensor readings. Unavailable data is reported honestly. Cache responses carry their age; expired responses may be displayed for up to two hours with a warning.",
        help_q3: "Что означает балл риска?",
        help_a3: "Heuristic 0–100 indices, not measured damage or calibrated probabilities. Overall <=35: low, >35 to 70: medium, >70: high. Water-deficit stress and waterlogging are separate.",
        help_q4: "Можно ли добавить новую локацию?",
        help_a4: "Локации настраиваются администратором. Обратитесь к команде платформы с GPS-координатами.",
        help_q5: "Что такое ET₀ (эвапотранспирация)?",
        help_a5: "Reference evapotranspiration is in mm/day. Open-Meteo daily FAO ET0 is used when explicitly filled. With no supplied ET0, analysis uses an uncalibrated temperature/humidity heuristic, not Penman-Monteith.",
        help_q6: "Как часто обновляются данные погоды?",
        help_a6: "The browser refresh interval controls requests. The server cache is fixed at 30 minutes; repeated refreshes may return the same timestamp. No API key is required.",
        help_support: "Контакты и поддержка", help_email: "Поддержка по email", help_phone: "Телефон",
        help_version: "SWIP 2.1 — synthetic-data demonstration, not field-validated guidance"
    },
    tg: {
        nav_subtitle: "Платформаи зеҳнии об ва\nобёрӣ",
        nav_dashboard: "Панел", nav_weather: "Обу ҳаво", nav_predictor: "Пешгӯикунанда",
        nav_risk: "Баҳодиҳии хавф", nav_water: "Идоракунии об", nav_field: "Замин ва хок",
        nav_analytics: "Таҳлил", nav_alerts: "Огоҳиҳо", nav_reports: "Ҳисоботҳо",
        nav_settings: "Танзимот", nav_help: "Кумак",
        last_updated: "Навсозӣ: --",
        dash_welcome: "Хуш омадед, Agri Guard",
        dash_desc: "Weather forecasts and user-entered analysis — not monitored farm observations.",
        kpi_water_need: "Final daily irrigation depth", kpi_water_stress: "Water-deficit index",
        kpi_drought_risk: "Daily dryness index", kpi_prediction: "Synthetic-model yield estimate",
        kpi_irrigation_req: "Run analysis for a final decision", kpi_low: "Паст", kpi_mod: "Мӯътадил", kpi_high: "Баланд",
        dash_live_weather: "Обу ҳавои ҳозира", dash_forecast: "Пешгӯии 7-рӯза",
        status_api_connected: "API обу ҳаво пайваст аст", ext_forecast: "Пешгӯии васеъ",
        pred_title: "Пешгӯии ҳосил ва обёрӣ бо ИИ", pred_live_inputs: "Daily analysis inputs",
        pred_autofill: "Enter daily values or explicitly use available forecast inputs. Soil moisture is never auto-observed.", pred_farm_info: "Маълумоти хоҷагӣ",
        lbl_temp: "Ҳарорат (°C)", lbl_rain: "Daily rainfall (mm)", lbl_hum: "Намнокӣ (%)",
        lbl_soil_moisture: "Намнокии хок (%)", lbl_crop: "Намуди зироат", lbl_soil: "Намуди хок",
        lbl_size: "Масоҳат (га)", lbl_growth_stage: "Марҳилаи рушд", btn_predict: "Пешгӯӣ кунед",
        opt_cotton: "Пахта", opt_wheat: "Гандум", opt_tomato: "Помидор", opt_potato: "Картошка",
        opt_sandy: "Регӣ", opt_loamy: "Хокдор", opt_clay: "Гилӣ",
        res_title: "Натиҷаи пешгӯӣ", res_risk: "Дараҷаи хавф:", res_water: "Оби лозим:",
        res_reasoning: "Decision explanation & limitations", res_yield: "Пешгӯии ҳосил:",
        badge_irrigate: "ОБЁРӢ КУНЕД", badge_no_irrigate: "ОБЁРӢ НАКУНЕД",
        data_source_live: "ЗИНДА", data_source_cache: "КЕШ", data_source_fallback: "UNAVAILABLE",
        data_source_estimated: "ТАХМИНӢ", data_source_sensor: "ДАТЧИК", data_source_manual: "ДАСТӢ",
        risk_overall: "Баҳои умумии хавф", risk_factors: "Омилҳои хавф",
        risk_drought: "Хатари хушксолӣ", risk_heat: "Стресси гармӣ",
        risk_water: "Стресси обӣ", risk_flood: "Хатари обхезӣ",
        risk_high: "ХАВФИ БАЛАНД", risk_moderate: "ХАВФИ МӮЪТАДИЛ", risk_low: "ХАВФИ ПАСТ",
        water_title: "Идоракунии об ва нақшаи обёрӣ",
        water_rec: "Forecast water-balance scenario — not an irrigation instruction",
        water_total: "Net depth total", water_avg: "Net depth per day", water_forecast: "Пешгӯии боришот",
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
        rep_predictions_made: "Пешгӯиҳои иҷрошуда", rep_all_time: "Latest 100 records (including unverified legacy records)",
        rep_generate: "Сохтани ҳисобот",
        rep_desc: "Export persisted analysis records. Volumes are recommendations, not metered consumption or proven savings.",
        rep_type: "Намуди ҳисобот", rep_period: "Давра", rep_format: "Формат",
        rep_opt_water: "Water requirement estimates", rep_opt_yield: "Хулосаи пешгӯии ҳосил",
        rep_opt_risk: "Heuristic risk history", rep_opt_irr: "Таърихи обёрӣ",
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
        help_about_text: "SWIP — Smart Water Intelligence Platform is a Tajikistan-focused demonstration. Open-Meteo provides modelled weather; all ML training inputs and targets in this repository are synthetic. No observed farm outcomes or field validation are available.",
        help_faq: "Саволҳои зуд-зуд пурсидашаванда",
        help_q1: "Тавсияи обёрӣ чӣ тавр ҳисоб мешавад?",
        help_a1: "A synthetic-target model is combined with an approximate daily water balance and safety overrides (>80% moisture or >30 mm daily rain). These legacy assumptions are not locally validated. Raw model and final rule-based decisions are shown separately.",
        help_q2: "Маълумоти обу ҳаво аз куҷо меояд?",
        help_a2: "Open-Meteo provides modelled current conditions and forecasts, not farm sensor readings. Unavailable data is reported honestly. Cache responses carry their age; expired responses may be displayed for up to two hours with a warning.",
        help_q3: "Баҳои хавф чӣ маънӣ дорад?",
        help_a3: "Heuristic 0–100 indices, not measured damage or calibrated probabilities. Overall <=35: low, >35 to 70: medium, >70: high. Water-deficit stress and waterlogging are separate.",
        help_q4: "Оё ман метавонам ҷойгиршавии нав илова кунам?",
        help_a4: "Ҷойгиршавиҳо аз тарафи администратор танзим мешаванд. Бо координатаҳои GPS муроҷиат кунед.",
        help_q5: "ET₀ (эвапотранспиратсия) чист?",
        help_a5: "Reference evapotranspiration is in mm/day. Open-Meteo daily FAO ET0 is used when explicitly filled. With no supplied ET0, analysis uses an uncalibrated temperature/humidity heuristic, not Penman-Monteith.",
        help_q6: "Маълумоти обу ҳаво чанд вақт як бор навсозӣ мешавад?",
        help_a6: "The browser refresh interval controls requests. The server cache is fixed at 30 minutes; repeated refreshes may return the same timestamp. No API key is required.",
        help_support: "Тамос ва дастгирӣ", help_email: "Дастгирӣ тавассути email", help_phone: "Телефон",
        help_version: "SWIP 2.1 — synthetic-data demonstration, not field-validated guidance"
    }
};

// ========== GLOBAL STATE ==========
const globalState = {
    weatherData: null, lastDecision: null, locationsList: [], lang: 'en',
    preferences: null, weatherSequence: 0, analysisSequence: 0,
    refreshTimer: null, weatherInputs: false
};
const byId = id => document.getElementById(id);
const text = (id, value) => { const el = byId(id); if (el) el.textContent = value; };
const numeric = value => typeof value === 'number' && Number.isFinite(value);
const format = (value, suffix = '') => numeric(value) ? value.toLocaleString(undefined, {maximumFractionDigits: 2}) + suffix : '—';
const icons = () => { if (typeof lucide !== 'undefined') lucide.createIcons(); };

function status(id, message, error = false) {
    const el = byId(id);
    if (el) {
        el.textContent = message;
        el.classList.toggle('text-danger', error);
    }
}

async function api(url, options = {}) {
    const response = await fetch(url, {...options, signal: AbortSignal.timeout(20000)});
    if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        const detail = typeof body.detail === 'string' ? body.detail :
            Array.isArray(body.detail) ? body.detail.map(error => error.msg).join('; ') : 'Request failed';
        throw new Error(detail);
    }
    return response;
}

function applyTranslations(lang) {
    globalState.lang = ['en', 'ru', 'tg'].includes(lang) ? lang : 'en';
    document.documentElement.lang = globalState.lang;
    const dict = T[globalState.lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        if (dict[el.dataset.i18n] !== undefined) el.textContent = dict[el.dataset.i18n];
    });
    byId('lang-select').value = globalState.lang;
    byId('settings-lang-select').value = globalState.lang;
    if (globalState.lastDecision) renderDecision(globalState.lastDecision);
    icons();
}

function activatePage(target) {
    document.querySelectorAll('.nav-links li').forEach(item => item.classList.toggle('active', item.dataset.target === target));
    document.querySelectorAll('.page-section').forEach(section => section.classList.toggle('active', section.id === target));
    byId('sidebar').classList.remove('is-open');
    byId('menu-toggle').setAttribute('aria-expanded', 'false');
    if (target === 'analytics' || target === 'reports') loadHistory();
    if (target === 'water') window.updateIrrigationChart(globalState.lastDecision?.plan);
}

function updateBackground(id) {
    const backgrounds = {khujand: 'agricultural_hills.jpg', sughd: 'agricultural_hills.jpg',
        bokhtar: 'cotton_plantation.jpg', khatlon: 'cotton_plantation.jpg',
        khorugh: 'reservoir_lake.jpg', badakhshan: 'reservoir_lake.jpg', drs: 'agricultural_hills.jpg'};
    byId('bg-layer').style.backgroundImage = "url('/static/images/" + (backgrounds[id] || 'pamir_mountain.jpg') + "')";
}

function clearDecision() {
    globalState.lastDecision = null;
    globalState.analysisSequence++;
    byId('prediction-result').style.display = 'none';
    ['dash-water-need', 'dash-water-stress', 'dash-drought-risk', 'dash-yield',
        'risk-overall-score', 'risk-overall-level', 'water-total', 'water-average', 'water-volume',
        'dash-drought-lvl', 'dash-stress-lvl'].forEach(id => text(id, '—'));
    ['drought-bar', 'heat-bar', 'water-bar', 'flood-bar', 'waterlogging-bar'].forEach(id => byId(id).style.width = '0%');
    ['drought-score', 'heat-score', 'water-score', 'flood-score', 'waterlogging-score'].forEach(id => text(id, '—'));
    text('field-summary', 'No current analysis. This application does not have registered fields or connected sensors.');
    text('alerts-list', 'Run an analysis to evaluate alerts. No connected sensor status is available.');
    text('dash-final-state', 'No current analysis');
    text('dash-water-subtext', 'Run analysis for a final decision');
    text('plan-status', 'Run analysis with an available forecast to generate a water-balance scenario.');
    window.updateIrrigationChart(null);
}

function clearWeather() {
    globalState.weatherData = null;
    ['dash-temp', 'dash-rain', 'dash-humidity', 'dash-wind', 'dash-et0', 'water-forecast-rain'].forEach(id => text(id, '—'));
    text('last-updated', 'No current weather response');
    text('weather-source-badge', 'UNAVAILABLE');
    text('weather-provider-state', 'Weather unavailable — manual analysis remains available.');
    text('dash-forecast', 'No forecast available.');
    text('extended-forecast', 'No forecast available.');
    byId('use-weather-btn').disabled = true;
    if (globalState.weatherInputs) {
        ['pred-temp', 'pred-rain', 'pred-humidity', 'pred-et0'].forEach(id => byId(id).value = '');
        text('input-source', 'Previous weather inputs cleared; enter daily values manually.');
        globalState.weatherInputs = false;
    }
}

function renderWeather(data) {
    const current = data.current;
    text('dash-temp', format(current.temperature, ' °C'));
    text('dash-rain', format(data.daily_rainfall_mm, ' mm/day'));
    text('dash-humidity', format(current.humidity, '%'));
    text('dash-wind', format(current.wind_speed, ' km/h'));
    text('dash-et0', format(data.et0, ' mm/day'));
    text('last-updated', 'Provider response retrieved: ' + new Date(data.timestamp).toLocaleString());
    text('weather-source-badge', data.data_source.toUpperCase() + (data.stale ? ' / STALE' : ''));
    text('weather-provider-state', 'Open-Meteo modelled conditions; ' + data.data_source + ', age ' + data.cache_age_seconds + ' seconds. Not a farm sensor.');
    text('water-forecast-rain', format(data.forecast.reduce((sum, day) => sum + day.precipitation, 0), ' mm'));
    for (const id of ['dash-forecast', 'extended-forecast']) {
        const container = byId(id);
        container.replaceChildren();
        for (const day of data.forecast) {
            const item = document.createElement('div');
            item.className = 'forecast-item';
            for (const label of [day.date, format(day.precipitation, ' mm'), format(day.max_temp, ' °C') + ' / ' + format(day.min_temp, ' °C')]) {
                const span = document.createElement('span');
                span.textContent = label;
                item.appendChild(span);
            }
            container.appendChild(item);
        }
    }
    byId('use-weather-btn').disabled = data.stale;
}

async function fetchWeather(locationId, fill = false) {
    const sequence = ++globalState.weatherSequence;
    byId('refresh-btn').disabled = true;
    clearDecision();
    clearWeather();
    status('weather-status', 'Loading Open-Meteo weather…');
    updateBackground(locationId);
    try {
        const response = await api('/api/weather?' + new URLSearchParams({location: locationId}));
        const data = await response.json();
        if (sequence !== globalState.weatherSequence) return;
        if (!data.current || !Array.isArray(data.forecast) || !data.forecast.length ||
            !numeric(data.current.temperature) || !numeric(data.daily_rainfall_mm) || !numeric(data.et0)) {
            throw new Error('Weather response incomplete; no substitute values generated.');
        }
        globalState.weatherData = data;
        renderWeather(data);
        status('weather-status', data.warning || 'Weather available. Modelled forecast; not a measured farm observation.', Boolean(data.stale));
        if (fill && !data.stale) fillWeatherInputs();
    } catch (error) {
        if (sequence !== globalState.weatherSequence) return;
        clearWeather();
        status('weather-status', 'Weather unavailable: ' + error.message + ' You can enter daily inputs manually.', true);
    } finally {
        if (sequence === globalState.weatherSequence) byId('refresh-btn').disabled = false;
    }
}

function fillWeatherInputs() {
    const data = globalState.weatherData;
    if (!data || data.stale) return;
    clearDecision();
    byId('pred-temp').value = data.current.temperature;
    byId('pred-humidity').value = data.current.humidity;
    byId('pred-rain').value = data.daily_rainfall_mm;
    byId('pred-et0').value = data.et0;
    globalState.weatherInputs = true;
    text('input-source', 'Temperature/humidity: provider current model; rainfall/ET0: today’s daily forecast. Soil moisture requires your entry or an explicit heuristic estimate.');
}

function populateSettings() {
    const prefs = globalState.preferences;
    byId('settings-default-loc').value = prefs.defaultLocation;
    byId('settings-refresh').value = prefs.refreshMinutes;
    byId('settings-lang-select').value = prefs.language;
}

function startRefreshTimer() {
    if (globalState.refreshTimer !== null) clearInterval(globalState.refreshTimer);
    globalState.refreshTimer = setInterval(() => {
        if (!document.hidden && byId('location-select').value) fetchWeather(byId('location-select').value);
    }, globalState.preferences.refreshMinutes * 60000);
}

async function savePreferences(reset = false) {
    try {
        const candidate = reset ? SWIPPreferences.defaults : {
            defaultLocation: byId('settings-default-loc').value,
            refreshMinutes: Number(byId('settings-refresh').value),
            language: byId('settings-lang-select').value
        };
        const saved = SWIPPreferences.save(localStorage, candidate, globalState.locationsList.map(location => location.id));
        globalState.preferences = saved;
        const changed = byId('location-select').value !== saved.defaultLocation;
        byId('location-select').value = saved.defaultLocation;
        populateSettings();
        applyTranslations(saved.language);
        startRefreshTimer();
        status('settings-status', reset ? 'Defaults restored and saved.' : 'Preferences saved in this browser.');
        if (changed) await fetchWeather(saved.defaultLocation, true);
    } catch (error) {
        status('settings-status', 'Preferences not saved: ' + error.message, true);
    }
}

function renderDecision(data) {
    const dict = T[globalState.lang];
    const recommended = data.decision.state === 'IRRIGATE';
    const finalLabel = recommended ? dict.badge_irrigate : dict.badge_no_irrigate;
    byId('prediction-result').style.display = 'block';
    text('res-badge', finalLabel);
    byId('res-badge').className = 'badge ' + (recommended ? 'irrigate' : 'do-not-irrigate');
    text('dash-final-state', finalLabel);
    text('res-raw-model', (data.model_irrigation.recommended ? dict.badge_irrigate : dict.badge_no_irrigate) +
        ' · uncalibrated class score ' + format(data.model_irrigation.probability, '%'));
    text('res-risk', format(data.risk.overall) + '/100 (' + data.risk.level + ')');
    text('res-water', format(data.irrigation.water_liters, ' L gross') + ' / ' + format(data.irrigation.amount_mm, ' mm net'));
    text('res-balance', format(data.water_balance.amount_mm, ' mm estimated deficit') + ' (separate from final instruction)');
    text('res-yield-value', format(data.yield.prediction_t_ha, ' t/ha') + '; tree spread ' +
        format(data.yield.range.lower) + '–' + format(data.yield.range.upper) + ' (not a calibrated interval)');
    text('res-soil-source', data.soil_status.source);
    byId('res-reasons-list').replaceChildren();
    for (const reason of data.explanations) {
        const item = document.createElement('li');
        item.textContent = reason;
        byId('res-reasons-list').appendChild(item);
    }
    text('dash-water-need', format(data.irrigation.amount_mm, ' mm net'));
    text('dash-water-subtext', 'Final action after model and safety rules; verify field conditions');
    text('dash-yield', format(data.yield.prediction_t_ha, ' t/ha'));
    text('dash-water-stress', format(data.risk.water_stress, '/100'));
    text('dash-drought-risk', format(data.risk.drought, '/100'));
    text('dash-drought-lvl', 'Heuristic daily index');
    text('dash-stress-lvl', 'Deficit index; waterlogging shown in Risk');
    text('risk-overall-score', format(data.risk.overall));
    text('risk-overall-level', data.risk.level + ' — heuristic, not probability');
    for (const [id, key] of [['drought', 'drought'], ['heat', 'heat'], ['water', 'water_stress'], ['flood', 'flood'], ['waterlogging', 'waterlogging']]) {
        byId(id + '-bar').style.width = Math.max(0, Math.min(100, data.risk[key])) + '%';
        text(id + '-score', format(data.risk[key], '/100'));
    }
    const plan = data.plan;
    text('plan-status', plan.meaning);
    text('water-total', format(plan.net_total_mm, ' mm'));
    text('water-average', plan.days?.length ? format(plan.net_total_mm / plan.days.length, ' mm/day') : '—');
    text('water-volume', format(plan.gross_total_liters, ' L'));
    window.updateIrrigationChart(plan);
    const payload = globalState.lastInputs;
    if (payload) text('field-summary', 'Latest submitted analysis — ' + payload.location + ', ' + payload.crop_type +
        ', ' + payload.soil_type + ', ' + payload.growth_stage + ', ' + payload.field_size + ' ha; moisture ' +
        data.soil_status.moisture_percent + '% (' + data.soil_status.source + '). No registered field or sensor connection is implied.');
    byId('alerts-list').replaceChildren();
    for (const alert of data.alerts || []) {
        const item = document.createElement('div');
        item.className = 'alert-item';
        const title = document.createElement('strong');
        const description = document.createElement('p');
        title.textContent = alert.title;
        description.textContent = alert.desc;
        item.append(title, description);
        byId('alerts-list').appendChild(item);
    }
    if (!data.alerts?.length) text('alerts-list', 'No alert thresholds triggered by this analysis. This is not a guarantee of field safety.');
}

function validDecision(data) {
    return ['IRRIGATE', 'DO_NOT_IRRIGATE'].includes(data.decision?.state) &&
        numeric(data.irrigation?.amount_mm) && numeric(data.irrigation?.water_liters) &&
        numeric(data.yield?.prediction_t_ha) && numeric(data.yield?.range?.lower) &&
        numeric(data.yield?.range?.upper) && numeric(data.risk?.overall) &&
        data.model_irrigation && data.water_balance && data.soil_status &&
        Array.isArray(data.explanations) && data.plan && Array.isArray(data.plan.days);
}

function setupPredictionForm() {
    const form = byId('prediction-form');
    form.addEventListener('input', event => {
        clearDecision();
        if (['pred-temp', 'pred-rain', 'pred-humidity', 'pred-et0'].includes(event.target.id)) {
            globalState.weatherInputs = false;
            text('input-source', 'User-edited daily weather inputs. Optional blank ET0 uses a labelled heuristic.');
        }
        status('analysis-status', 'Inputs changed — run analysis again.');
    });
    byId('pred-soil-source').addEventListener('change', () => {
        const estimated = byId('pred-soil-source').value === 'estimated';
        byId('pred-soil-moisture').required = !estimated;
        byId('pred-soil-moisture').disabled = estimated;
    });
    form.addEventListener('submit', async event => {
        event.preventDefault();
        if (!form.reportValidity() || byId('analyze-btn').disabled) return;
        clearDecision();
        const sequence = globalState.analysisSequence;
        const location = byId('location-select');
        const payload = {
            location: location.selectedOptions[0]?.textContent || 'Manual location',
            weather_location: location.value || null,
            temperature: Number(byId('pred-temp').value), rainfall: Number(byId('pred-rain').value),
            humidity: Number(byId('pred-humidity').value),
            soil_moisture: byId('pred-soil-source').value === 'estimated' ? null : Number(byId('pred-soil-moisture').value),
            soil_moisture_source: byId('pred-soil-source').value,
            crop_type: byId('pred-crop').value, soil_type: byId('pred-soil').value,
            field_size: Number(byId('pred-size').value), growth_stage: byId('pred-growth-stage').value,
            et0_mm: byId('pred-et0').value === '' ? null : Number(byId('pred-et0').value), language: globalState.lang
        };
        byId('analyze-btn').disabled = true;
        byId('analyze-btn').setAttribute('aria-busy', 'true');
        status('analysis-status', 'Analysing and saving…');
        try {
            const response = await api('/api/decision', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
            const data = await response.json();
            if (sequence !== globalState.analysisSequence) {
                status('analysis-status', 'Inputs changed while analysis ran. The completed request may be in history; analyse again for current inputs.');
                return;
            }
            if (!validDecision(data)) throw new Error('Incomplete analysis response. No result displayed.');
            globalState.lastDecision = data;
            globalState.lastInputs = payload;
            renderDecision(data);
            status('analysis-status', 'Analysis saved as history record ' + data.history_id + '. Demonstration estimate, not field-validated guidance.');
            loadHistory();
        } catch (error) {
            if (sequence === globalState.analysisSequence) {
                clearDecision();
                status('analysis-status', 'Analysis failed: ' + error.message, true);
            }
        } finally {
            byId('analyze-btn').disabled = false;
            byId('analyze-btn').setAttribute('aria-busy', 'false');
        }
    });
}

async function loadHistory() {
    const body = byId('history-table').querySelector('tbody');
    body.replaceChildren();
    text('rep-pred-count', '—');
    try {
        const response = await api('/api/history?limit=100');
        const data = await response.json();
        if (!Array.isArray(data.history)) throw new Error('History response incomplete');
        text('history-status', data.warning);
        text('rep-pred-count', data.history.length);
        for (const row of data.history) {
            const tr = document.createElement('tr');
            const stamp = row.timestamp ? new Date(row.timestamp) : null;
            const values = [stamp && !Number.isNaN(stamp.getTime()) ? stamp.toLocaleString() : 'Unknown date',
                row.crop_type || '—', format(row.soil_moisture, '%'),
                row.prediction === 1 ? T[globalState.lang].hist_irrigate : T[globalState.lang].hist_wait,
                format(row.risk_score, '/100'), row.provenance === 'legacy_unverified' ? 'Legacy / unverified' : 'Synthetic-model estimate'];
            for (const value of values) {
                const cell = document.createElement('td');
                cell.textContent = value;
                tr.appendChild(cell);
            }
            body.appendChild(tr);
        }
        if (!data.history.length) {
            const row = body.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 6;
            cell.textContent = 'No prediction history yet. Run an analysis to create a record.';
        }
    } catch (error) {
        body.replaceChildren();
        status('history-status', 'History unavailable: ' + error.message, true);
    }
}

async function downloadReport() {
    const button = byId('report-download-btn');
    if (button.disabled) return;
    const limit = Number(byId('report-limit').value);
    if (!Number.isInteger(limit) || limit < 1 || limit > 1000) {
        status('report-status', 'Record limit must be a whole number between 1 and 1000.', true);
        return;
    }
    const params = new URLSearchParams({report_type: byId('report-type-select').value,
        period: byId('report-period-select').value, format: byId('report-format').value, limit});
    button.disabled = true;
    status('report-status', 'Generating CSV…');
    try {
        const response = await api('/api/report?' + params);
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'swip_' + byId('report-type-select').value + '_' + byId('report-period-select').value + '.csv';
        document.body.appendChild(link);
        link.click();
        link.remove();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        status('report-status', 'CSV generated from ' + response.headers.get('X-Report-Record-Count') + ' persisted records. Empty reports contain headers only.');
    } catch (error) {
        status('report-status', 'Report failed: ' + error.message, true);
    } finally {
        button.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    icons();
    clearDecision();
    document.querySelectorAll('.nav-links li a').forEach(link => {
        link.addEventListener('click', event => { event.preventDefault(); activatePage(link.parentElement.dataset.target); });
    });
    byId('menu-toggle').addEventListener('click', () => {
        const open = byId('sidebar').classList.toggle('is-open');
        byId('menu-toggle').setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && byId('sidebar').classList.contains('is-open')) {
            byId('sidebar').classList.remove('is-open');
            byId('menu-toggle').setAttribute('aria-expanded', 'false');
            byId('menu-toggle').focus();
        }
    });
    byId('location-select').addEventListener('change', event => fetchWeather(event.target.value, true));
    byId('refresh-btn').addEventListener('click', () => fetchWeather(byId('location-select').value));
    byId('use-weather-btn').addEventListener('click', fillWeatherInputs);
    byId('settings-save').addEventListener('click', () => savePreferences());
    byId('settings-reset').addEventListener('click', () => savePreferences(true));
    byId('report-download-btn').addEventListener('click', downloadReport);
    byId('lang-select').addEventListener('change', event => {
        applyTranslations(event.target.value);
        try {
            globalState.preferences = SWIPPreferences.save(localStorage,
                {...globalState.preferences, language: event.target.value}, globalState.locationsList.map(location => location.id));
        } catch (error) { status('settings-status', 'Language changed for this page only: ' + error.message, true); }
        loadHistory();
    });
    setupPredictionForm();
    loadHistory();
    try {
        const response = await api('/api/locations');
        const locations = await response.json();
        if (!Array.isArray(locations) || !locations.length) throw new Error('No configured locations available');
        globalState.locationsList = locations;
        for (const id of ['location-select', 'settings-default-loc']) {
            byId(id).replaceChildren();
            for (const location of locations) byId(id).add(new Option(location.name, location.id));
        }
        let loaded;
        try { loaded = SWIPPreferences.load(localStorage, locations.map(location => location.id)); }
        catch (error) { loaded = {value: {...SWIPPreferences.defaults}, warning: error.message}; }
        globalState.preferences = loaded.value;
        populateSettings();
        applyTranslations(loaded.value.language);
        if (loaded.warning) status('settings-status', loaded.warning, true);
        byId('location-select').value = loaded.value.defaultLocation;
        startRefreshTimer();
        await fetchWeather(loaded.value.defaultLocation, true);
    } catch (error) {
        clearWeather();
        status('weather-status', 'Location list unavailable: ' + error.message + '. Manual analysis remains available.', true);
        globalState.preferences = {...SWIPPreferences.defaults};
    }
    try {
        const response = await api('/api/data-sources');
        const source = await response.json();
        text('provenance-status', source.dataset
            ? source.dataset.name + ': ' + source.dataset.rows + ' static rows. ' + source.warnings.join(' ')
            : 'Operational metadata unavailable. Model provenance must be verified before presenting results.');
    } catch (error) {
        status('provenance-status', 'Metadata unavailable: ' + error.message, true);
    }
});
