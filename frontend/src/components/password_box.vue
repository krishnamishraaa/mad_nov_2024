<template>
    <div class="password-container">
        <!-- Password Input -->
        <div>
            <label for="password">Password:</label>
            <input id="password" v-model="password" type="password" required
                :class="{ 'invalid': !isPasswordValid && password.length > 0 }" />
            <div v-if="password.length > 0">
                <small v-if="password.length < 8">Password must be at least 8 characters.</small>
                <small v-if="!hasUpperCase">Password must contain at least one uppercase letter.</small>
                <small v-if="!hasNumber">Password must contain at least one number.</small>
            </div>
        </div>

        <!-- Confirm Password Input -->
        <div>
            <label for="confirm-password">Confirm Password:</label>
            <input id="confirm-password" v-model="confirmPassword" type="password" required
                :class="{ 'invalid': !doPasswordsMatch && confirmPassword.length > 0 }" />
            <div v-if="confirmPassword.length > 0">
                <small v-if="!doPasswordsMatch">Passwords do not match.</small>
            </div>
        </div>

        <!-- Valid Message -->
        <div v-if="isFormValid" class="valid-message">
            Passwords are valid and match!
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, defineEmits } from 'vue';

// Emits
const emit = defineEmits(['update:modelValue', 'valid-password']);

const password = ref('');
const confirmPassword = ref('');

// Validation rules
const hasUpperCase = computed(() => /[A-Z]/.test(password.value));
const hasNumber = computed(() => /\d/.test(password.value));
const isPasswordValid = computed(() => {
    const minLength = 8;
    return password.value.length >= minLength && hasUpperCase.value && hasNumber.value;
});
const doPasswordsMatch = computed(() => password.value === confirmPassword.value);
const isFormValid = computed(() => isPasswordValid.value && doPasswordsMatch.value);

// Emit password to parent when valid
watch([password, confirmPassword], () => {
    if (isFormValid.value) {
        emit('update:modelValue', password.value); // Bind password to v-model
        emit('valid-password', true); // Notify parent about valid password
    } else {
        emit('valid-password', false); // Notify parent about invalid password
    }
});
</script>

<style scoped>
label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

input.invalid {
    border-color: #e74c3c;
}

small {
    color: #e74c3c;
    font-size: 12px;
}

.valid-message {
    color: #2ecc71;
    font-weight: bold;
}

div {
    margin-bottom: 15px;
}
</style>
