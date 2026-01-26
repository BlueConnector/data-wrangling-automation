// Student progress management
class ProgressTracker {
    constructor() {
        this.progress = this.loadProgress();
    }
    
    loadProgress() {
        const saved = localStorage.getItem('dataWranglingProgress');
        return saved ? JSON.parse(saved) : {};
    }
    
    saveProgress() {
        localStorage.setItem('dataWranglingProgress', JSON.stringify(this.progress));
    }
    
    updateExerciseProgress(exerciseId, completed) {
        this.progress[exerciseId] = completed;
        this.saveProgress();
    }
    
    getCompletionRate() {
        const total = Object.keys(this.progress).length;
        const completed = Object.values(this.progress).filter(Boolean).length;
        return total > 0 ? (completed / total) * 100 : 0;
    }
}