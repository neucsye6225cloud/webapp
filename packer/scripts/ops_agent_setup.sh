#!/bin/bash

curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install

sudo chown -R csye6225:csye6225 /etc/google-cloud-ops-agent/

sudo tee /etc/google-cloud-ops-agent/config.yaml > /dev/null <<EOF
logging:
  receivers:
    my-app-receiver:
      type: files
      include_paths:
        - /var/log/blogapp/myapp.log
      record_log_file_path: true
      json_logging:
        enable_json_parsing: true
        timestamp_format: "%Y-%m-%dT%H:%M:%S.%L%Z"
  processors:
    my-app-processor:
      type: parse_json
      time_key: time
      time_format: "%Y-%m-%dT%H:%M:%S.%L%Z"
      severity_key: severity
      severity_map:
        INFO: "INFO"
        DEBUG: "DEBUG"
        ERROR: "ERROR"
        WARN: "WARNING"
  service:
    pipelines:
      default_pipeline:
        receivers: [my-app-receiver]
        processors: [my-app-processor]
EOF

sudo systemctl restart google-cloud-ops-agent
