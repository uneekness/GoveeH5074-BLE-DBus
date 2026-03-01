#!/usr/bin/env python3
import asyncio
from govee_ble import Govee
from dbus_next.aio import MessageBus
from dbus_next import Variant

UPDATE_INTERVAL = 10  # seconds

async def main():
    bus = await MessageBus().connect()
    govee = Govee()

    while True:
        print("Scanning for Govee H5074 sensors...")
        devices = govee.scan()
        sensors = [d for d in devices if d.model == "H5074"]

        if not sensors:
            print("No H5074 sensors found! Retrying in 10s...")
            await asyncio.sleep(UPDATE_INTERVAL)
            continue

        for sensor in sensors:
            try:
                data = sensor.get_data()
                sensor_name_temp = f"Govee_{sensor.mac.replace(':','')}_T"
                sensor_name_hum = f"Govee_{sensor.mac.replace(':','')}_H"

                await bus.call(
                    bus.message_to_send(
                        f"/com/victronenergy/sensors/{sensor_name_temp}/temperature",
                        "com.victronenergy.BusItem.SetValue",
                        Variant('d', data['temperature'])
                    )
                )
                await bus.call(
                    bus.message_to_send(
                        f"/com/victronenergy/sensors/{sensor_name_hum}/humidity",
                        "com.victronenergy.BusItem.SetValue",
                        Variant('d', data['humidity'])
                    )
                )
                print(f"{sensor.mac}: T={data['temperature']}°C, H={data['humidity']}%")
            except Exception as e:
                print(f"Error reading {sensor.mac}: {e}")

        await asyncio.sleep(UPDATE_INTERVAL)

asyncio.run(main())
