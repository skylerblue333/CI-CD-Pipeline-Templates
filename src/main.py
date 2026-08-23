"""CI/CD template registry for the SKYCOIN4444 developer platform."""
from __future__ import annotations

import time
from threading import RLock

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="SKYCOIN4444 CI/CD Template Registry", version="3.1.0")


class PipelineTemplate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    language: str = Field(min_length=1, max_length=50)
    stages: list[str] = Field(min_length=1, max_length=20)
    triggers: list[str] = Field(min_length=1, max_length=20)

    def normalized(self) -> "PipelineTemplate":
        return self.model_copy(
            update={
                "name": self.name.strip(),
                "language": self.language.strip(),
                "stages": [stage.strip() for stage in self.stages if stage.strip()],
                "triggers": [trigger.strip() for trigger in self.triggers if trigger.strip()],
            }
        )


templates: dict[str, PipelineTemplate] = {}
_lock = RLock()


@app.post("/api/v1/templates", status_code=status.HTTP_201_CREATED)
def create_template(template: PipelineTemplate):
    template = template.normalized()
    if not template.stages or not template.triggers:
        raise HTTPException(status_code=422, detail="stages and triggers must contain values")
    with _lock:
        if template.name in templates:
            raise HTTPException(status_code=409, detail="Template already exists")
        templates[template.name] = template
    return {"status": "created", "name": template.name}


@app.get("/api/v1/templates/{name}")
def get_template(name: str):
    with _lock:
        template = templates.get(name)
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return template.model_dump()


@app.get("/api/v1/templates")
def list_templates():
    with _lock:
        return [template.model_dump() for template in templates.values()]


@app.delete("/api/v1/templates/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(name: str):
    with _lock:
        if templates.pop(name, None) is None:
            raise HTTPException(status_code=404, detail="Template not found")


@app.get("/health")
def health():
    return {"status": "healthy", "service": "CI-CD-Pipeline-Templates", "timestamp": int(time.time())}
