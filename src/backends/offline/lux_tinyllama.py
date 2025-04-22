import random
import threading
import time
import json
import math
import itertools
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
try:
    from numba import jit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Função Numba para variações ópticas
if NUMBA_AVAILABLE:
    @jit(nopython=True)
    def generate_combinations(freq_start, freq_end, freq_step, mod_count, pol_count, intens_count, max_variations):
        variations = []
        count = 0
        for freq in range(freq_start, freq_end, freq_step):
            for mod in range(mod_count):
                for pol in range(pol_count):
                    for intens in range(intens_count):
                        variations.append((freq, mod, pol, intens))
                        count += 1
                        if count >= max_variations:
                            return variations
        return variations

class KnowledgeRepository:
    def __init__(self):
        self.messages = []
        self.lock = threading.Lock()

    def add_message(self, message):
        with self.lock:
            self.messages.append(message)

    def get_messages(self, agent_id):
        with self.lock:
            return [msg for msg in self.messages if msg["sender"] != agent_id]

class TinyLLaMAAgent:
    def __init__(self, id, channel, repository):
        self.id = id
        self.channel = channel
        self.repository = repository
        self.messages_sent = 0
        self.messages_received = 0
        self.message_log = []
        self.lock = threading.Lock()
        if TRANSFORMERS_AVAILABLE:
            self.tokenizer = AutoTokenizer.from_pretrained("TinyLLaMA/TinyLLaMA-1.1B-Chat-v1.0")
            self.model = AutoModelForCausalLM.from_pretrained("TinyLLaMA/TinyLLaMA-1.1B-Chat-v1.0")
        else:
            raise ImportError("Transformers não instalado. Instale com: pip install transformers torch")

    def generate_message(self, context=None):
        if not TRANSFORMERS_AVAILABLE:
            return "Mensagem de teste (TinyLLaMA não disponível)"
        prompt = "Você é um agente colaborativo em um sistema de IAG social. Gere uma mensagem criativa para iniciar ou responder a uma colaboração. "
        if context:
            prompt += f"Contexto: {context}\nResponda de forma natural e colaborativa:"
        else:
            prompt += "Inicie com uma ideia colaborativa:"
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=50, num_return_probs=1, do_sample=True, temperature=0.7)
        message = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return message.strip()

    def send_message(self, content=None):
        if content is None:
            content = self.generate_message()
        binary_message = self.to_binary(content)
        optical_variations = self.generate_optical_variations(content)
        message = {
            "sender": self.id,
            "timestamp": time.time_ns(),
            "content": content,
            "binary": binary_message,
            "optical_variations": optical_variations[:5]
        }
        with self.lock:
            self.messages_sent += 1
            self.message_log.append(message)
        self.repository.add_message(message)
        for _ in range(500):  # Trabalho extra
            math.sin(random.random())

    def consult_repository(self):
        messages = self.repository.get_messages(self.id)
        with self.lock:
            for msg in messages:
                if (msg["sender"], msg["timestamp"]) not in [(m["sender"], m["timestamp"]) for m in self.message_log]:
                    self.messages_received += 1
                    self.message_log.append(msg)
                    # Responde contextualmente com TinyLLaMA
                    response_content = self.generate_message(context=msg["content"])
                    self.send_message(content=response_content)

    def to_binary(self, message):
        return ' '.join(format(ord(c), '08b') for c in message)

    def generate_optical_variations(self, message, max_variations=50):
        frequencies = range(400, 600, 20)
        modulations = ['AM', 'FM', 'PM']
        polarizations = ['horizontal', 'vertical']
        intensities = [1, 2, 3]
        if NUMBA_AVAILABLE:
            combos = generate_combinations(400, 600, 20, len(modulations), len(polarizations), len(intensities), max_variations)
            variations = [
                f"{message} | Freq: {combo[0]} THz | Mod: {modulations[int(combo[1])]} | Pol: {polarizations[int(combo[2])]} | Intens: {intensities[int(combo[3])]}"
                for combo in combos
            ]
        else:
            variations = []
            for freq, mod, pol, intens in itertools.product(frequencies, modulations, polarizations, intensities):
                variations.append(f"{message} | Freq: {freq} THz | Mod: {mod} | Pol: {pol} | Intens: {intens}")
                if len(variations) >= max_variations:
                    break
        return variations

def monitor_resources(max_cpu=50.0, max_mem_mb=256.0):
    if not PSUTIL_AVAILABLE:
        return True
    process = psutil.Process()
    cpu_usage = psutil.cpu_percent(percpu=True)
    avg_cpu = sum(cpu_usage) / len(cpu_usage)
    mem_usage = process.memory_info().rss / 1024 / 1024
    return avg_cpu <= max_cpu and mem_usage <= max_mem_mb

def simulate_lux_computer(num_agents=2):
    repository = KnowledgeRepository()
    agents = [TinyLLaMAAgent(f"TinyLLaMAAgent-{i+1}", 400 + i * 0.3, repository) for i in range(num_agents)]

    total_messages_sent = 0
    total_messages_received = 0
    start_time = time.time()

    cpu_usages = []
    if PSUTIL_AVAILABLE:
        process = psutil.Process()
        mem_start = process.memory_info().rss / 1024 / 1024

    def agent_task(agent):
        while not monitor_resources():
            time.sleep(0.1)
        agent.send_message()  # Inicia com uma mensagem gerada
        agent.consult_repository()  # Consulta e responde contextualmente
        if PSUTIL_AVAILABLE:
            cpu_usages.append(psutil.cpu_percent(percpu=True))

    threads = []
    for agent in agents:
        thread = threading.Thread(target=agent_task, args=(agent,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    agent_metrics = []
    for agent in agents:
        total_messages_sent += agent.messages_sent
        total_messages_received += agent.messages_received
        agent_metrics.append({
            "agent_id": agent.id,
            "messages_sent": agent.messages_sent,
            "messages_received": agent.messages_received
        })

    end_time = time.time()
    duration = end_time - start_time

    channels_possible = num_agents * 3 * 2 * 3
    channels_in_use = min(num_agents * 50, channels_possible)

    message_log = []
    for agent in agents:
        message_log.extend(agent.message_log)

    metrics = {
        "total_agents": num_agents,
        "messages_sent": total_messages_sent,
        "messages_received": total_messages_received,
        "agent_metrics": agent_metrics,
        "simulation_duration_seconds": round(duration, 2),
        "channels_possible": {
            "optical_combinations": channels_possible
        },
        "channels_in_use": {
            "optical_combinations": channels_in_use
        },
        "messages_exchanged": message_log
    }

    if PSUTIL_AVAILABLE:
        mem_end = process.memory_info().rss / 1024 / 1024
        cpu_usage_avg = [sum([cpu[i] for cpu in cpu_usages]) / len(cpu_usages) for i in range(len(cpu_usages[0]))] if cpu_usages else [0.0] * 8
        avg_cpu = sum(cpu_usage_avg) / len(cpu_usage_avg)
        energy_estimate = avg_cpu * duration * 0.0001
        metrics["memory_usage_mb"] = round(mem_end - mem_start, 2)
        metrics["cpu_usage_per_core"] = [round(x, 1) for x in cpu_usage_avg]
        metrics["energy_consumption_kwh"] = round(energy_estimate, 6)
    else:
        metrics["memory_usage_mb"] = round(num_agents * 0.1, 2)
        metrics["cpu_usage_per_core"] = "Not available"
        metrics["energy_consumption_kwh"] = round(duration * 0.00005, 6)

    print("\n=== Métricas Finais ===")
    print(f"Total de agentes: {metrics['total_agents']}")
    print("Métricas por agente:")
    for agent in agent_metrics:
        print(f"  Agente {agent['agent_id']}:")
        print(f"    Mensagens enviadas: {agent['messages_sent']}")
        print(f"    Mensagens recebidas: {agent['messages_received']}")
    print(f"Mensagens totais enviadas: {metrics['messages_sent']}")
    print(f"Mensagens totais recebidas: {metrics['messages_received']}")
    print(f"Duração da simulação: {metrics['simulation_duration_seconds']:.2f} segundos")
    print(f"Canais possíveis: {metrics['channels_possible']}")
    print(f"Canais em uso: {metrics['channels_in_use']}")
    if PSUTIL_AVAILABLE:
        print(f"Consumo de memória: {metrics['memory_usage_mb']:.2f} MB")
        print(f"Uso de CPU por núcleo: {metrics['cpu_usage_per_core']}")
        print(f"Consumo de energia estimado: {metrics['energy_consumption_kwh']:.6f} kWh")
    else:
        print(f"Estimativa de memória: ~{metrics['memory_usage_mb']:.2f} MB")
        print(f"Uso de CPU por núcleo: {metrics['cpu_usage_per_core']}")
        print(f"Estimativa de energia: ~{metrics['energy_consumption_kwh']:.6f} kWh")

    try:
        with open("lux_metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)
        print("\nMétricas e mensagens salvas em 'lux_metrics.json'")
    except Exception as e:
        print(f"\nErro ao salvar JSON: {e}")

    return metrics

if __name__ == "__main__":
    simulate_lux_computer(num_agents=2)