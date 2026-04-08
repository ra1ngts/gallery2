import { stateCtx } from './store.svelte';

// formateDate
export function formateDate(date) {
    if (!date) return '...';

    const dateObj = new Date(date);

    if (isNaN(dateObj.getTime())) {
        console.error(`Error date formatting: ${date}`);
        return 'Date not found';
    }

    return dateObj.toLocaleDateString('ru-RU', { month: '2-digit', year: 'numeric' }).replace('.', ' / ');
}

// getDuration
export function getDuration(startDate, endDate, isCurrent) {
    const start = formateDate(startDate);
    
    if (isCurrent || !endDate) {
        return `${start} — ${stateCtx.translation.utils?.present}`;
    }
    
    const end = formateDate(endDate);
    return `${start} — ${end}`;
}

// Email address validation
export function isEmailValidate(email) {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    // console.log('isEmailValidate:', pattern.test(email));
    return pattern.test(email);
}

// Check touched field
export function markAsTouched(field) {
    stateCtx.touchedFields[field] = true;
    checkFields();
}

// checkFields
export function checkFields() {
    if (stateCtx.contactsData.name === '') {
        stateCtx.formErrors['name'] = stateCtx.translation.contact?.errors.name;
    } else {
        delete stateCtx.formErrors['name'];
    }

    if (!isEmailValidate(stateCtx.contactsData.email) || stateCtx.contactsData.email === '') {
        stateCtx.formErrors['email'] = stateCtx.translation.contact?.errors.email;
    } else {
        delete stateCtx.formErrors['email'];
    }

    if (stateCtx.contactsData.subject === '') {
        stateCtx.formErrors['subject'] = stateCtx.translation.contact?.errors.subject;
    } else {
        delete stateCtx.formErrors['subject'];
    }

    if (stateCtx.contactsData.message === '') {
        stateCtx.formErrors['message'] = stateCtx.translation.contact?.errors.message;
    } else {
        delete stateCtx.formErrors['message'];
    }
}

// showToast
export function showToast(message, type = 'success') {
    stateCtx.toast = { show: true, message, type };

    setTimeout(() => {
        stateCtx.toast.show = false;
    }, 3000);
}