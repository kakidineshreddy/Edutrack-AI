/* Dashboard Graphical Panels Builder (Chart.js Defaults & Inits) */

// Global configuration defaults for dark theme representation
const applyGlobalChartDefaults = () => {
  if (typeof Chart === 'undefined') return;

  Chart.defaults.color = '#a0a0b0';
  Chart.defaults.font.family = "'Outfit', sans-serif";
  Chart.defaults.font.size = 12;
  Chart.defaults.responsive = true;
  Chart.defaults.maintainAspectRatio = false;

  // Custom tooltips styling
  Chart.defaults.plugins.tooltip = {
    ...Chart.defaults.plugins.tooltip,
    backgroundColor: 'rgba(26, 26, 46, 0.95)',
    titleColor: '#ffffff',
    bodyColor: '#ffffff',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderWidth: 1,
    padding: 12,
    cornerRadius: 8,
    displayColors: true
  };
};

// 1. Grade Trend Chart (Line Plot)
const initGradeTrendChart = (canvasId, data) => {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext('2d');
  
  applyGlobalChartDefaults();

  // Create beautiful gradient fill under the line
  const purpleGradient = ctx.createLinearGradient(0, 0, 0, 300);
  purpleGradient.addColorStop(0, 'rgba(108, 99, 255, 0.45)');
  purpleGradient.addColorStop(1, 'rgba(108, 99, 255, 0.00)');

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels || ['Month 1', 'Month 2', 'Month 3'],
      datasets: [{
        label: 'Average Score',
        data: data.values || [70, 78, 85],
        borderColor: '#6c63ff',
        borderWidth: 3,
        pointBackgroundColor: '#00d4ff',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        fill: true,
        backgroundColor: purpleGradient,
        tension: 0.4
      }]
    },
    options: {
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#a0a0b0' }
        },
        y: {
          min: 0,
          max: 100,
          grid: { color: 'rgba(255, 255, 255, 0.03)' },
          ticks: { color: '#a0a0b0' }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
};

// 2. Attendance Chart (Doughnut Plot)
const initAttendanceChart = (canvasId, data) => {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext('2d');
  
  applyGlobalChartDefaults();

  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Present', 'Absent', 'Late'],
      datasets: [{
        data: data.values || [85, 10, 5],
        backgroundColor: [
          '#00d68f', // success green
          '#ff4d6d', // danger red
          '#ffaa00'  // warning yellow
        ],
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      cutout: '72%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            boxWidth: 12,
            padding: 20,
            color: '#a0a0b0'
          }
        }
      }
    }
  });
};

// 3. Subject Performance Chart (Horizontal Bar Plot)
const initSubjectChart = (canvasId, data) => {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext('2d');
  
  applyGlobalChartDefaults();

  const cyanGradient = ctx.createLinearGradient(0, 0, 300, 0);
  cyanGradient.addColorStop(0, '#6c63ff');
  cyanGradient.addColorStop(1, '#00d4ff');

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.subjects || ['Mathematics', 'Science', 'English', 'Computer Science'],
      datasets: [{
        label: 'Average Score',
        data: data.scores || [80, 85, 75, 90],
        backgroundColor: cyanGradient,
        borderRadius: 8,
        borderSkipped: false,
        barPercentage: 0.65
      }]
    },
    options: {
      indexAxis: 'y',
      scales: {
        x: {
          min: 0,
          max: 100,
          grid: { color: 'rgba(255, 255, 255, 0.03)' },
          ticks: { color: '#a0a0b0' }
        },
        y: {
          grid: { display: false },
          ticks: { color: '#a0a0b0' }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
};

// 4. Performance radar representation (Radar Plot)
const initPerformanceChart = (canvasId, data) => {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext('2d');
  
  applyGlobalChartDefaults();

  return new Chart(ctx, {
    type: 'radar',
    data: {
      labels: data.subjects || ['Math', 'Science', 'English', 'CS', 'General'],
      datasets: [{
        label: 'Current Level',
        data: data.scores || [80, 75, 90, 85, 95],
        backgroundColor: 'rgba(0, 212, 255, 0.15)',
        borderColor: '#00d4ff',
        borderWidth: 2,
        pointBackgroundColor: '#00d4ff',
        pointBorderColor: '#ffffff',
        pointRadius: 4
      }]
    },
    options: {
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.05)' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          pointLabels: { color: '#a0a0b0', font: { size: 11 } },
          ticks: { backdropColor: 'transparent', color: '#a0a0b0' },
          suggestedMin: 0,
          suggestedMax: 100
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
};
