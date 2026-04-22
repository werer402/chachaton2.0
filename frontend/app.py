import streamlit as st
import streamlit.components.v1 as components
import requests
import json

API_URL = "http://localhost:8000"
st.set_page_config(page_title="MTB City Pro", layout="wide")

if "user_id" not in st.session_state: st.session_state.user_id = None
if "mode" not in st.session_state: st.session_state.mode = "farm"

# --- UI Styles ---
st.markdown("""
<style>
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #f8f9fa; padding: 10px; border-top: 1px solid #ddd; z-index: 100; display: flex; justify-content: space-around; }
    .stButton button { width: 100%; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.user_id:
    st.title("🏦 MTB City: Вход")
    name = st.text_input("Введите ваше имя:")
    if st.button("Начать"):
        requests.post(f"{API_URL}/user/register", params={"user_id": name.lower(), "username": name})
        st.session_state.user_id = name.lower()
        st.rerun()
else:
    # Загрузка данных
    user = requests.get(f"{API_URL}/user/{st.session_state.user_id}").json()
    
    # Sidebar
    st.sidebar.metric("🪙 Коины", f"{user['mt_coins']:.1f}")
    st.sidebar.metric("💳 Траты", f"{user['total_spent']:.1f} BYN")
    
    if st.session_state.mode == "farm":
        st.title("🏙️ 3D МТБ-Сити")
        
        # Подготовка данных для 3D
        farm_data = requests.get(f"{API_URL}/farm/buildings/{st.session_state.user_id}").json()
        
        # Встраиваем 3D Движок
        components.html(f"""
            <div id="three-container" style="width: 100%; height: 500px; border-radius: 20px; background: #90caf9;"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script>
                const farmData = {json.dumps(farm_data)};
                const container = document.getElementById('three-container');
                
                const scene = new THREE.Scene();
                scene.background = new THREE.Color(0x90caf9);
                
                const camera = new THREE.PerspectiveCamera(50, container.clientWidth/500, 0.1, 1000);
                camera.position.set(7, 7, 7);
                camera.lookAt(0, 0, 0);

                const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(container.clientWidth, 500);
                container.appendChild(renderer.domElement);

                scene.add(new THREE.AmbientLight(0xffffff, 0.6));
                const sun = new THREE.DirectionalLight(0xffffff, 0.8);
                sun.position.set(10, 20, 10);
                scene.add(sun);

                // Сетка координат для зданий
                const coords = {{
                    "mtb_bank": [0,0], "wildberries": [-2,2], "steam": [2,2], 
                    "yandex_go": [-2,-2], "burger_king": [2,-2], "mak_by": [0,3]
                }};
                
                const colors = {{
                    "mtb_bank": 0x0d47a1, "wildberries": 0x7b1fa2, "steam": 0x263238,
                    "yandex_go": 0xfbc02d, "burger_king": 0xd84315, "mak_by": 0x2e7d32
                }};

                // Отрисовка
                farmData.forEach(item => {{
                    const pos = coords[item.info.company_id];
                    const isBuilt = item.state !== null;
                    
                    if (isBuilt) {{
                        const h = item.state.level * 0.6 + 0.4;
                        const geo = new THREE.BoxGeometry(1.2, h, 1.2);
                        const mat = new THREE.MeshPhongMaterial({{ color: colors[item.info.company_id] }});
                        const mesh = new THREE.Mesh(geo, mat);
                        mesh.position.set(pos[0], h/2, pos[1]);
                        scene.add(mesh);
                    }} else {{
                        // Фундамент для нераскрытых
                        const geo = new THREE.PlaneGeometry(1.2, 1.2);
                        const mat = new THREE.MeshBasicMaterial({{ color: 0xffffff, transparent: true, opacity: 0.3, side: THREE.DoubleSide }});
                        const mesh = new THREE.Mesh(geo, mat);
                        mesh.rotation.x = Math.PI / 2;
                        mesh.position.set(pos[0], 0.01, pos[1]);
                        scene.add(mesh);
                    }}
                }});

                // Пол
                const ground = new THREE.Mesh(new THREE.PlaneGeometry(15, 15), new THREE.MeshPhongMaterial({{color: 0x81c784}}));
                ground.rotation.x = -Math.PI / 2;
                scene.add(ground);

                function animate() {{
                    requestAnimationFrame(animate);
                    scene.rotation.y += 0.003;
                    renderer.render(scene, camera);
                }}
                animate();
            </script>
        """, height=520)

        st.divider()
        with st.expander("💳 Симуляция оплаты картой"):
            c1, c2 = st.columns(2)
            target = c1.selectbox("Компания", ["wildberries", "steam", "yandex_go", "burger_king", "mak_by"])
            amt = c2.number_input("Сумма покупки", 10, 1000, 100)
            if st.button("Оплатить"):
                requests.post(f"{API_URL}/farm/add-spending", params={{"user_id": user['user_id'], "company_id": target, "amount": amt}})
                st.rerun()

    elif st.session_state.mode == "shop":
        st.title("🎁 Твои призы")
        for code in user['inventory']: st.success(code)

    # Навигация (Bottom Bar)
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("📊 ЛИДЕРЫ"): st.session_state.mode = "leaderboard"; st.rerun()
    if c2.button("🛍️ МАГАЗИН"): st.session_state.mode = "shop"; st.rerun()
    if c3.button("🏙️ ГОРОД"): st.session_state.mode = "farm"; st.rerun()
    if c4.button("⚔️ ФАЙТ"): st.session_state.mode = "fight"; st.rerun()