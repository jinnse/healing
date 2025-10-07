# Healing Scope

## 프로젝트 개요
Self-Healing 및 실시간 모니터링이 구현된 Kubernetes 기반 인프라 프로젝트

## 프로젝트 목적
- Kubernetes의 Self-Healing 및 모니터링 원리 실습 및 시각화
- 장애 유발 → 자동 복구 → 모니터링/알림까지의 실전 DevOps 사이클 
- PVC, NFS, Slack 연동 등 클라우드 네이티브 인프라 구성

## 인프라 구성

<img width="1201" height="521" alt="Image" src="https://github.com/user-attachments/assets/7927040c-33c1-4596-89d6-e1853fd6fd1f" />
>
> *위 이미지는 Healing Scope의 인프라 구성도를 나타냅니다.*

- **주요 컴포넌트**: K8s, NFS Server, PVC, Prometheus, Alertmanager, Slack, 앱 컨테이너
- **인프라 흐름 요약**:  
  앱 장애 → Liveness/Readiness → Restart/복구 → 로그/PVC → NFS 백업 → Prometheus/Alertmanager → Slack 알림

## 디렉토리 구조

## 작동 구성 방식

1. Kubernetes에 앱/스토리지/모니터링 구성 배포
2. 의도적으로 앱에 장애 유발
3. K8s Liveness/Readiness Probe로 장애 탐지 및 Pod 자동 복구
4. Prometheus/Alertmanager가 Pod 상태 실시간 모니터링, Alert 발생
5. Alertmanager가 Slack 채널로 장애/복구 알림 전송
6. 앱 로그는 PVC로 마운트, NFS 서버에 저장/백업

## 백업 및 로그 관리

- PVC로 마운트된 로그 디렉토리를 NFS 서버에 실시간/주기 백업
- 장애/복구 시 로그 유실 방지, 재현성 보장

## 기대효과

- **서비스 안정성 및 무중단 운영 실현**  
  Pod, 애플리케이션 장애가 발생해도 Kubernetes의 Self-Healing 기능을 통해 자동으로 문제를 복구하므로, 서비스의 중단 시간을 최소화.

- **운영 효율성 및 장애 대응 속도 향상**  
  Prometheus 및 Alertmanager를 활용한 실시간 모니터링과 자동화된 알림 시스템(Slack 연동)으로, 운영자는 장애를 즉시 인지하고 신속하게 대응.

- **데이터 보호 및 장애 시 신속한 복구 기반 확보**  
  로그와 데이터를 PVC-NFS 구조로 별도 보관/백업함으로써, 장애나 재배포, 서버 교체 상황에서도 중요한 데이터 유실을 방지할 수 있다.

- **운영 자동화 수준 향상**  
  장애 감지부터 복구, 알림, 로그 백업까지 전 과정이 자동화되어 인적 개입을 최소화.

## 기술 스택
1. Kubernetes
2. Prometheus/Alertmanager/Grafana
3. NFS Server
4. Python(Flask), Docker
5. Slack Webhook
