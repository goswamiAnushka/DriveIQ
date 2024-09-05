export const generateSuggestions = (drivingData) => {
    const suggestions = [];
    const avgScore = drivingData.reduce((acc, d) => acc + d.score, 0) / drivingData.length;
    
    if (avgScore > 70) {
      suggestions.push('Your driving score is high. Try to reduce aggressive driving.');
    } else if (avgScore < 50) {
      suggestions.push('Great job! Keep up the safe driving.');
    }
  
    return suggestions;
  };
  