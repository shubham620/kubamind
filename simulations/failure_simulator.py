"""
CPU Spike Simulation
"""

import asyncio
import random
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def simulate_cpu_spike(duration_seconds: int = 60, intensity: float = 0.9):
    """
    Simulate a CPU spike in a pod
    
    Args:
        duration_seconds: How long the spike lasts
        intensity: Severity of the spike (0.0-1.0)
    """
    logger.info(f"🔴 Simulating CPU spike for {duration_seconds}s")
    
    start_time = datetime.utcnow()
    
    # Simulate elevated CPU
    while (datetime.utcnow() - start_time).total_seconds() < duration_seconds:
        cpu_usage = 50 + (intensity * 45)  # 50-95% CPU
        logger.info(f"CPU Usage: {cpu_usage:.1f}%")
        await asyncio.sleep(1)
    
    logger.info("✓ CPU spike simulation complete")


async def simulate_memory_leak(hours: int = 2, leak_rate_mb_per_hour: float = 10):
    """
    Simulate a memory leak
    
    Args:
        hours: Duration of simulation
        leak_rate_mb_per_hour: Memory leak rate
    """
    logger.info(f"🔴 Simulating memory leak for {hours} hours")
    
    initial_memory_mb = 256
    current_memory = initial_memory_mb
    
    for hour in range(hours):
        for minute in range(60):
            current_memory += leak_rate_mb_per_hour / 60
            if minute % 5 == 0:
                logger.info(f"Memory: {current_memory:.1f} MB / 512 MB")
            await asyncio.sleep(0.5)  # Speed up simulation
    
    logger.info(f"✓ Final memory: {current_memory:.1f} MB")


async def simulate_pod_crash():
    """Simulate a pod crash"""
    logger.info("🔴 Simulating pod crash")
    await asyncio.sleep(2)
    logger.info("✓ Pod crashed and restarting...")
    await asyncio.sleep(1)
    logger.info("✓ Pod restarted successfully")


async def simulate_storage_fill(hours: int = 4, growth_percent_per_hour: float = 5):
    """
    Simulate storage being filled
    
    Args:
        hours: Duration of simulation
        growth_percent_per_hour: Storage growth rate
    """
    logger.info(f"🔴 Simulating storage fill for {hours} hours")
    
    current_usage = 30
    
    for hour in range(hours):
        for minute in range(60):
            current_usage += growth_percent_per_hour / 60
            if minute % 5 == 0:
                logger.info(f"Storage: {current_usage:.1f}% / 100%")
            await asyncio.sleep(0.5)  # Speed up
    
    logger.info(f"✓ Storage full at {current_usage:.1f}%")


async def simulate_network_latency(spike_duration_seconds: int = 30, latency_ms: float = 500):
    """
    Simulate network latency spike
    
    Args:
        spike_duration_seconds: How long the spike lasts
        latency_ms: Latency in milliseconds
    """
    logger.info(f"🔴 Simulating network latency spike ({latency_ms}ms)")
    
    for _ in range(spike_duration_seconds):
        actual_latency = latency_ms + random.uniform(-100, 100)
        logger.info(f"Latency: {actual_latency:.0f}ms")
        await asyncio.sleep(1)
    
    logger.info("✓ Network latency normalized")


async def run_all_simulations():
    """Run all simulations sequentially"""
    logger.info("Starting infrastructure failure simulations...")
    
    # Run simulations with short durations for demo
    await simulate_cpu_spike(duration_seconds=5, intensity=0.85)
    logger.info("")
    
    await simulate_memory_leak(hours=1, leak_rate_mb_per_hour=20)  # Speeds up in 30 seconds
    logger.info("")
    
    await simulate_pod_crash()
    logger.info("")
    
    await simulate_storage_fill(hours=1, growth_percent_per_hour=20)  # Speeds up
    logger.info("")
    
    await simulate_network_latency(spike_duration_seconds=5, latency_ms=250)
    
    logger.info("\n✅ All simulations complete!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_all_simulations())
