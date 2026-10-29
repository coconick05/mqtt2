import paho.mqtt.client as paho
import streamlit as st
import json
import uuid
import platform

st.write("Versión de Python:", platform.python_version())

broker = "157.230.214.127"
port = 1883


def crear_cliente():
    # ID único para no chocar con otros clientes del broker público
    client_id = "GIT-HUB-" + uuid.uuid4().hex[:8]
    try:
        # paho-mqtt 2.x
        return paho.Client(paho.CallbackAPIVersion.VERSION1, client_id)
    except AttributeError:
        # paho-mqtt 1.x
        return paho.Client(client_id)


def publicar(topic, mensaje):
    try:
        cliente = crear_cliente()
        cliente.connect(broker, port, 60)
        cliente.loop_start()
        info = cliente.publish(topic, json.dumps(mensaje))
        info.wait_for_publish(timeout=5)
        cliente.loop_stop()
        cliente.disconnect()
        st.success(f"Enviado a {topic}: {json.dumps(mensaje)}")
    except Exception as e:
        st.error(f"Error al publicar: {e}")


st.title("MQTT Control")

col1, col2 = st.columns(2)

with col1:
    if st.button("ON"):
        publicar("cmqtt_s", {"Act1": "ON"})

with col2:
    if st.button("OFF"):
        publicar("cmqtt_s", {"Act1": "OFF"})

values = st.slider("Selecciona el rango de valores", 0.0, 100.0)
st.write("Values:", values)

if st.button("Enviar valor analógico"):
    publicar("cmqtt_a", {"Analog": float(values)})
