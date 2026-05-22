/* Three.js neon cybernetic background scene */

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("bg");
  if (!canvas) return;

  // 1. Scene, Camera & Renderer Setup
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x0f0f1a, 0.08);

  const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.z = 6;

  const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: true,
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);

  // 2. Lighting Infrastructure
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.45);
  scene.add(ambientLight);

  const pointLightPurple = new THREE.PointLight(0x6c63ff, 2.5, 30);
  pointLightPurple.position.set(5, 5, 2);
  scene.add(pointLightPurple);

  const pointLightCyan = new THREE.PointLight(0x00d4ff, 2.5, 30);
  pointLightCyan.position.set(-5, -5, 2);
  scene.add(pointLightCyan);

  // 3. Floating Mesh Arrays (5 Spheres, 5 Boxes, 5 Octahedrons)
  const meshes = [];
  const geometries = [
    new THREE.SphereGeometry(0.4, 32, 32),
    new THREE.BoxGeometry(0.6, 0.6, 0.6),
    new THREE.OctahedronGeometry(0.5, 0),
  ];

  const colors = [0x6c63ff, 0x00d4ff, 0x3b82f6];

  // Spawn 15 meshes randomly
  for (let i = 0; i < 15; i++) {
    const geo = geometries[i % geometries.length];
    const color = colors[i % colors.length];

    // Wireframe Mesh for premium cybernetic vector aesthetic
    const material = new THREE.MeshPhongMaterial({
      color: color,
      emissive: color,
      emissiveIntensity: 0.3,
      wireframe: true,
      transparent: true,
      opacity: 0.65,
    });

    const mesh = new THREE.Mesh(geo, material);

    // Randomize initial positions
    mesh.position.x = (Math.random() - 0.5) * 12;
    mesh.position.y = (Math.random() - 0.5) * 8;
    mesh.position.z = (Math.random() - 0.5) * 6;

    // Save initial coordinates for floating animations
    mesh.userData = {
      baseY: mesh.position.y,
      floatSpeed: 0.5 + Math.random() * 1.5,
      floatAmplitude: 0.15 + Math.random() * 0.25,
      rotSpeedX: (Math.random() - 0.5) * 0.015,
      rotSpeedY: (Math.random() - 0.5) * 0.015,
    };

    scene.add(mesh);
    meshes.push(mesh);
  }

  // 4. Particle System (1000 stars)
  const particleCount = 1000;
  const particleGeometry = new THREE.BufferGeometry();
  const particlePositions = new Float32Array(particleCount * 3);

  for (let i = 0; i < particleCount * 3; i += 3) {
    particlePositions[i] = (Math.random() - 0.5) * 20;     // X
    particlePositions[i + 1] = (Math.random() - 0.5) * 20; // Y
    particlePositions[i + 2] = (Math.random() - 0.5) * 10; // Z
  }

  particleGeometry.setAttribute(
    "position",
    new THREE.BufferAttribute(particlePositions, 3)
  );

  // High performance particle points
  const particleMaterial = new THREE.PointsMaterial({
    size: 0.025,
    color: 0x00d4ff,
    transparent: true,
    opacity: 0.75,
    blending: THREE.AdditiveBlending,
  });

  const particleSystem = new THREE.Points(particleGeometry, particleMaterial);
  scene.add(particleSystem);

  // 5. Responsive Resize Event Listener
  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  });

  // 6. Animation Render Loop
  const clock = new THREE.Clock();

  const animate = () => {
    requestAnimationFrame(animate);

    const elapsedTime = clock.getElapsedTime();

    // Animate meshes (Rotation & Floating)
    meshes.forEach((mesh) => {
      mesh.rotation.x += mesh.userData.rotSpeedX;
      mesh.rotation.y += mesh.userData.rotSpeedY;

      // Harmonic vertical floating math
      mesh.position.y =
        mesh.userData.baseY +
        Math.sin(elapsedTime * mesh.userData.floatSpeed) *
          mesh.userData.floatAmplitude;
    });

    // Slow rotation of entire particle cluster
    particleSystem.rotation.y = elapsedTime * 0.025;
    particleSystem.rotation.x = elapsedTime * 0.01;

    renderer.render(scene, camera);
  };

  animate();
});
