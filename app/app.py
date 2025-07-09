from flask import Flask
import os
import time
import logging
import threading

app = Flask(__name__)

# 로그 설정
LOG_DIR = "/app/logs"
LOG_FILE = f"{LOG_DIR}/app.log"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 상태 플래그
is_started = True
is_ready = True
is_healthy = True

# 자동 복구 함수
def auto_readiness_recovery():
    time.sleep(120)
    global is_ready
    is_ready = True
    logging.info("자동 복구: readiness 상태를 True로 변경함")

def auto_liveness_recovery():
    time.sleep(60)
    global is_healthy
    is_healthy = True
    logging.info("자동 복구: liveness 상태를 True로 변경함")

@app.route('/')
def home():
    logging.info("홈 요청")
    return "Hello, I'm alive!"

@app.route('/healthz')
def health():
    if is_healthy:
        logging.info("liveness 체크 - OK")
        return "OK", 200
    else:
        logging.error("liveness 체크 - FAIL")
        return "Unhealthy", 503

@app.route('/ready')
def ready():
    if is_ready:
        logging.info("readiness 체크 - Ready")
        return "Ready", 200
    else:
        logging.warning("readiness 체크 - Not Ready")
        return "Not Ready", 503

@app.route('/startup')
def startup():
    if is_started:
        return "Started", 200
    else:
        return "Starting", 503

# Liveness 테스트용 (자동 복구 포함)
@app.route('/simulate_liveness_failure')
def simulate_liveness_failure():
    global is_healthy
    is_healthy = False
    logging.warning("liveness 상태를 False로 설정함")

    # 30초 후 자동 복구 스레드 실행
    recovery_thread = threading.Thread(target=auto_liveness_recovery)
    recovery_thread.daemon = True
    recovery_thread.start()

    return "Liveness failure simulated, will auto-recover in 30s", 200

# Readiness 테스트용 (자동 복구 포함)
@app.route('/simulate_dependency_failure')
def simulate_dependency_failure():
    global is_ready
    is_ready = False
    logging.warning("readiness 상태를 False로 설정함")

    recovery_thread = threading.Thread(target=auto_readiness_recovery)
    recovery_thread.daemon = True
    recovery_thread.start()

    return "Readiness failure simulated, will auto-recover in 30s", 200

# 수동 복구용
@app.route('/init')
def init():
    global is_started, is_ready, is_healthy
    logging.info("앱 상태를 Started, Ready, Healthy로 초기화함")
    is_started = True
    is_ready = True
    is_healthy = True
    return "App initialized", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
