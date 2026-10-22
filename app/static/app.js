const state = {
    notes: [],
    selectedNoteId: null,
    toastTimer: null,
    searchTimer: null,
};


const elements = {
    noteForm: document.querySelector("#noteForm"),
    noteFormTitle: document.querySelector("#noteFormTitle"),
    editingNoteId: document.querySelector("#editingNoteId"),

    noteTitle: document.querySelector("#noteTitle"),
    noteDate: document.querySelector("#noteDate"),
    noteSource: document.querySelector("#noteSource"),
    noteClassification: document.querySelector(
        "#noteClassification"
    ),
    noteDiscipline: document.querySelector("#noteDiscipline"),
    noteLocation: document.querySelector("#noteLocation"),
    noteTags: document.querySelector("#noteTags"),
    noteReliability: document.querySelector(
        "#noteReliability"
    ),
    noteCredibility: document.querySelector(
        "#noteCredibility"
    ),
    noteBody: document.querySelector("#noteBody"),

    cancelEditButton: document.querySelector(
        "#cancelEditButton"
    ),
    refreshButton: document.querySelector("#refreshButton"),
    clearFiltersButton: document.querySelector(
        "#clearFiltersButton"
    ),

    searchInput: document.querySelector("#searchInput"),
    classificationFilter: document.querySelector(
        "#classificationFilter"
    ),
    disciplineFilter: document.querySelector(
        "#disciplineFilter"
    ),
    reliabilityFilter: document.querySelector(
        "#reliabilityFilter"
    ),
    credibilityFilter: document.querySelector(
        "#credibilityFilter"
    ),
    locationFilter: document.querySelector(
        "#locationFilter"
    ),
    startDateFilter: document.querySelector(
        "#startDateFilter"
    ),
    endDateFilter: document.querySelector(
        "#endDateFilter"
    ),

    noteList: document.querySelector("#noteList"),

    totalNotes: document.querySelector("#totalNotes"),
    osintNotes: document.querySelector("#osintNotes"),
    highReliabilityNotes: document.querySelector(
        "#highReliabilityNotes"
    ),
    restrictedNotes: document.querySelector(
        "#restrictedNotes"
    ),

    noteDetailWorkspace: document.querySelector(
        "#noteDetailWorkspace"
    ),
    detailTitle: document.querySelector("#detailTitle"),
    noteDetail: document.querySelector("#noteDetail"),
    closeDetailButton: document.querySelector(
        "#closeDetailButton"
    ),

    toast: document.querySelector("#toast"),
};


function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function valueOrNull(value) {
    const normalizedValue = String(value ?? "").trim();

    return normalizedValue || null;
}


function formatDisplayDate(value) {
    if (!value) {
        return "Not specified";
    }

    const parts = String(value).split("-");

    if (parts.length !== 3) {
        return value;
    }

    return `${parts[1]}/${parts[2]}/${parts[0]}`;
}


function getToday() {
    const today = new Date();
    const offset = today.getTimezoneOffset() * 60_000;
    const localDate = new Date(today.getTime() - offset);

    return localDate.toISOString().split("T")[0];
}


function showToast(message, isError = false) {
    window.clearTimeout(state.toastTimer);

    elements.toast.textContent = message;
    elements.toast.classList.remove("hidden");
    elements.toast.classList.toggle("error", isError);

    state.toastTimer = window.setTimeout(() => {
        elements.toast.classList.add("hidden");
        elements.toast.classList.remove("error");
    }, 3500);
}


async function requestJson(url, options = {}) {
    const response = await fetch(url, options);

    if (response.status === 204) {
        return null;
    }

    let data = null;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        let message = "The request could not be completed.";

        if (typeof data?.detail === "string") {
            message = data.detail;
        } else if (Array.isArray(data?.detail)) {
            message = data.detail
                .map((error) => error.msg)
                .join(" ");
        }

        throw new Error(message);
    }

    return data;
}


function buildFilterQuery() {
    const query = new URLSearchParams();

    const filters = {
        keyword: elements.searchInput.value.trim(),
        classification:
            elements.classificationFilter.value,
        discipline: elements.disciplineFilter.value,
        reliability: elements.reliabilityFilter.value,
        credibility: elements.credibilityFilter.value,
        location: elements.locationFilter.value.trim(),
        start_date: elements.startDateFilter.value,
        end_date: elements.endDateFilter.value,
    };

    Object.entries(filters).forEach(([key, value]) => {
        if (value) {
            query.set(key, value);
        }
    });

    const queryString = query.toString();

    return queryString ? `?${queryString}` : "";
}


async function loadStatistics() {
    try {
        const notes = await requestJson("/notes");

        elements.totalNotes.textContent = notes.length;

        elements.osintNotes.textContent = notes.filter(
            (note) => note.discipline === "OSINT"
        ).length;

        elements.highReliabilityNotes.textContent =
            notes.filter(
                (note) =>
                    note.reliability === "A" ||
                    note.reliability === "B"
            ).length;

        elements.restrictedNotes.textContent = notes.filter(
            (note) =>
                note.classification &&
                note.classification !== "UNCLASSIFIED"
        ).length;
    } catch (error) {
        showToast(
            `Unable to load statistics: ${error.message}`,
            true
        );
    }
}


function buildBadge(
    value,
    className = ""
) {
    if (!value) {
        return "";
    }

    return `
        <span class="badge ${className}">
            ${escapeHtml(value)}
        </span>
    `;
}


function renderNotes() {
    if (state.notes.length === 0) {
        elements.noteList.innerHTML = `
            <p class="empty-state">
                No intelligence notes match the current filters.
            </p>
        `;

        return;
    }

    elements.noteList.innerHTML = state.notes
        .map((note) => {
            const evaluation =
                note.reliability || note.credibility
                    ? `${
                        note.reliability || "—"
                    }${note.credibility || "—"}`
                    : null;

            return `
                <article class="note-card">
                    <div class="note-card-header">
                        <h3>
                            ${escapeHtml(note.title)}
                        </h3>

                        <span class="note-date">
                            ${escapeHtml(
                                formatDisplayDate(note.date)
                            )}
                        </span>
                    </div>

                    <div class="metadata-row">
                        ${buildBadge(
                            note.classification,
                            "classification"
                        )}

                        ${buildBadge(
                            note.discipline,
                            "discipline"
                        )}

                        ${buildBadge(
                            evaluation,
                            "evaluation"
                        )}

                        ${buildBadge(note.location)}
                    </div>

                    <p class="note-card-body">
                        ${
                            note.body
                                ? escapeHtml(note.body)
                                : "No narrative recorded."
                        }
                    </p>

                    <div class="note-card-actions">
                        <button
                            class="action-button"
                            type="button"
                            data-action="view"
                            data-note-id="${note.id}"
                        >
                            View
                        </button>

                        <button
                            class="action-button"
                            type="button"
                            data-action="edit"
                            data-note-id="${note.id}"
                        >
                            Edit
                        </button>

                        <button
                            class="danger-button action-button"
                            type="button"
                            data-action="delete"
                            data-note-id="${note.id}"
                        >
                            Delete
                        </button>
                    </div>
                </article>
            `;
        })
        .join("");
}


async function loadNotes() {
    elements.noteList.innerHTML = `
        <p class="empty-state">
            Loading intelligence notes...
        </p>
    `;

    try {
        state.notes = await requestJson(
            `/notes${buildFilterQuery()}`
        );

        renderNotes();
    } catch (error) {
        state.notes = [];

        elements.noteList.innerHTML = `
            <p class="empty-state">
                Unable to load intelligence notes.
            </p>
        `;

        showToast(
            `Unable to load notes: ${error.message}`,
            true
        );
    }
}


function getFormData() {
    return {
        title: elements.noteTitle.value.trim(),
        date: valueOrNull(elements.noteDate.value),
        source: valueOrNull(elements.noteSource.value),
        classification: valueOrNull(
            elements.noteClassification.value
        ),
        discipline: valueOrNull(
            elements.noteDiscipline.value
        ),
        location: valueOrNull(elements.noteLocation.value),
        tags: valueOrNull(elements.noteTags.value),
        reliability: valueOrNull(
            elements.noteReliability.value
        ),
        credibility: valueOrNull(
            elements.noteCredibility.value
        ),
        body: valueOrNull(elements.noteBody.value),
    };
}


function resetForm() {
    elements.noteForm.reset();
    elements.editingNoteId.value = "";
    elements.noteFormTitle.textContent = (
        "Create Intelligence Note"
    );

    elements.cancelEditButton.classList.add("hidden");
    elements.noteDate.value = getToday();
}


function populateForm(note) {
    elements.editingNoteId.value = note.id;
    elements.noteTitle.value = note.title || "";
    elements.noteDate.value = note.date || "";
    elements.noteSource.value = note.source || "";

    elements.noteClassification.value =
        note.classification || "";

    elements.noteDiscipline.value =
        note.discipline || "";

    elements.noteLocation.value = note.location || "";
    elements.noteTags.value = note.tags || "";

    elements.noteReliability.value =
        note.reliability || "";

    elements.noteCredibility.value =
        note.credibility || "";

    elements.noteBody.value = note.body || "";

    elements.noteFormTitle.textContent = (
        "Edit Intelligence Note"
    );

    elements.cancelEditButton.classList.remove("hidden");

    elements.noteForm.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });

    elements.noteTitle.focus();
}


async function saveNote(event) {
    event.preventDefault();

    const noteData = getFormData();
    const editingNoteId = elements.editingNoteId.value;

    const url = editingNoteId
        ? `/notes/${editingNoteId}`
        : "/notes";

    const method = editingNoteId
        ? "PATCH"
        : "POST";

    try {
        await requestJson(url, {
            method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(noteData),
        });

        showToast(
            editingNoteId
                ? "Intelligence note updated."
                : "Intelligence note created."
        );

        resetForm();

        await Promise.all([
            loadNotes(),
            loadStatistics(),
        ]);
    } catch (error) {
        showToast(
            `Unable to save note: ${error.message}`,
            true
        );
    }
}


function renderNoteDetail(note) {
    const evaluation = (
        note.reliability || note.credibility
    )
        ? `${
            note.reliability || "—"
        }${note.credibility || "—"}`
        : "Not evaluated";

    elements.detailTitle.textContent = note.title;

    elements.noteDetail.innerHTML = `
        <div class="detail-metadata">
            <div class="detail-field">
                <span>Reporting Date</span>
                <strong>
                    ${escapeHtml(
                        formatDisplayDate(note.date)
                    )}
                </strong>
            </div>

            <div class="detail-field">
                <span>Classification</span>
                <strong>
                    ${escapeHtml(
                        note.classification ||
                        "Not specified"
                    )}
                </strong>
            </div>

            <div class="detail-field">
                <span>Discipline</span>
                <strong>
                    ${escapeHtml(
                        note.discipline ||
                        "Not specified"
                    )}
                </strong>
            </div>

            <div class="detail-field">
                <span>Source Evaluation</span>
                <strong>
                    ${escapeHtml(evaluation)}
                </strong>
            </div>

            <div class="detail-field">
                <span>Source</span>
                <strong>
                    ${escapeHtml(
                        note.source ||
                        "Not specified"
                    )}
                </strong>
            </div>

            <div class="detail-field">
                <span>Location</span>
                <strong>
                    ${escapeHtml(
                        note.location ||
                        "Not specified"
                    )}
                </strong>
            </div>

            <div class="detail-field">
                <span>Tags</span>
                <strong>
                    ${escapeHtml(
                        note.tags ||
                        "None"
                    )}
                </strong>
            </div>

            <div class="detail-field">
                <span>Record ID</span>
                <strong>
                    ${escapeHtml(note.id)}
                </strong>
            </div>
        </div>

        <section class="detail-section">
            <h3>Intelligence Note</h3>

            <p>
                ${
                    note.body
                        ? escapeHtml(note.body)
                        : "No narrative recorded."
                }
            </p>
        </section>
    `;

    elements.noteDetailWorkspace.classList.remove("hidden");

    elements.noteDetailWorkspace.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });
}


async function viewNote(noteId) {
    try {
        const note = await requestJson(
            `/notes/${noteId}`
        );

        state.selectedNoteId = note.id;

        renderNoteDetail(note);
    } catch (error) {
        showToast(
            `Unable to load note: ${error.message}`,
            true
        );
    }
}


async function editNote(noteId) {
    try {
        const note = await requestJson(
            `/notes/${noteId}`
        );

        populateForm(note);
    } catch (error) {
        showToast(
            `Unable to load note: ${error.message}`,
            true
        );
    }
}


async function deleteNote(noteId) {
    const note = state.notes.find(
        (item) => item.id === noteId
    );

    const noteTitle = note?.title || "this note";

    const confirmed = window.confirm(
        `Delete "${noteTitle}"? This action cannot be undone.`
    );

    if (!confirmed) {
        return;
    }

    try {
        await requestJson(
            `/notes/${noteId}`,
            {
                method: "DELETE",
            }
        );

        if (state.selectedNoteId === noteId) {
            closeDetail();
        }

        if (
            Number(elements.editingNoteId.value) === noteId
        ) {
            resetForm();
        }

        showToast("Intelligence note deleted.");

        await Promise.all([
            loadNotes(),
            loadStatistics(),
        ]);
    } catch (error) {
        showToast(
            `Unable to delete note: ${error.message}`,
            true
        );
    }
}


function handleNoteListClick(event) {
    const button = event.target.closest(
        "button[data-action]"
    );

    if (!button) {
        return;
    }

    const noteId = Number(button.dataset.noteId);
    const action = button.dataset.action;

    if (!Number.isInteger(noteId)) {
        return;
    }

    if (action === "view") {
        viewNote(noteId);
    }

    if (action === "edit") {
        editNote(noteId);
    }

    if (action === "delete") {
        deleteNote(noteId);
    }
}


function closeDetail() {
    state.selectedNoteId = null;

    elements.noteDetailWorkspace.classList.add("hidden");
    elements.detailTitle.textContent = "Intelligence Note";
    elements.noteDetail.innerHTML = "";
}


function clearFilters() {
    elements.searchInput.value = "";
    elements.classificationFilter.value = "";
    elements.disciplineFilter.value = "";
    elements.reliabilityFilter.value = "";
    elements.credibilityFilter.value = "";
    elements.locationFilter.value = "";
    elements.startDateFilter.value = "";
    elements.endDateFilter.value = "";

    loadNotes();
}


function queueSearch() {
    window.clearTimeout(state.searchTimer);

    state.searchTimer = window.setTimeout(() => {
        loadNotes();
    }, 300);
}


function registerEventListeners() {
    elements.noteForm.addEventListener(
        "submit",
        saveNote
    );

    elements.cancelEditButton.addEventListener(
        "click",
        resetForm
    );

    elements.refreshButton.addEventListener(
        "click",
        async () => {
            await Promise.all([
                loadNotes(),
                loadStatistics(),
            ]);

            showToast("Intelligence holdings refreshed.");
        }
    );

    elements.clearFiltersButton.addEventListener(
        "click",
        clearFilters
    );

    elements.noteList.addEventListener(
        "click",
        handleNoteListClick
    );

    elements.closeDetailButton.addEventListener(
        "click",
        closeDetail
    );

    elements.searchInput.addEventListener(
        "input",
        queueSearch
    );

    elements.locationFilter.addEventListener(
        "input",
        queueSearch
    );

    [
        elements.classificationFilter,
        elements.disciplineFilter,
        elements.reliabilityFilter,
        elements.credibilityFilter,
        elements.startDateFilter,
        elements.endDateFilter,
    ].forEach((filterElement) => {
        filterElement.addEventListener(
            "change",
            loadNotes
        );
    });
}


async function initializeApplication() {
    elements.noteDate.value = getToday();

    registerEventListeners();

    await Promise.all([
        loadNotes(),
        loadStatistics(),
    ]);
}


initializeApplication();