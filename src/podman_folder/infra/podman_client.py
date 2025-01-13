from contextlib import contextmanager
import podman


@contextmanager
def get_podman_client(url: str):
    client=None
    try:
        client = podman.PodmanClient(base_url=url) #ctrl+click en PodmanClient para ver los key attributes que se le pueden poner
        yield client
        
    except Exception as e:
        print(f"Error initializing Podman client: {e}")  # Manejo de errores de inicialización
    finally:
        if client is not None:  # si fue inicializado, lo cerramos
            client.close()