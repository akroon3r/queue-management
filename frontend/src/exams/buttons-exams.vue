<template v-if="showExams">
  <div style="display: flex; justify-content: flex-start; width: 100%">
    <div style="flex-grow: 12">
      <b-form inline>
        <b-button variant="primary" class="mr-1" @click="clickAddIndividual">Add Individual Exam</b-button>
        <b-button variant="primary" class="mr-1" @click="clickAddNonITA">Add Non-ITA Exam</b-button>
        <b-button variant="primary" v-if="liaison" @click="clickAddGroup">Add Group Exam</b-button>
      </b-form>
    </div>
    <div style="flex-grow: 1">
      <b-button variant="primary" @click="clickGenFinReport">Generate Financial Report</b-button>
    </div>
    <AddExamFormModal />
    <FinancialReportModal />
  </div>
</template>

<script>
  import { mapMutations, mapState, mapGetters } from 'vuex'
  import AddExamFormModal from './add-exam-form-modal'
  import FinancialReportModal from './generate-financial-report-modal'

  export default {
    name: "ButtonsExams",
    components: {AddExamFormModal, FinancialReportModal },
    computed: {
      ...mapState([ 'user',
                    'showGenFinReportModal',
                    'addNonITA' ]),
      ...mapGetters([ 'showExams', ]),
      liaison() {
        if (this.user && this.user.role) {
          return (this.user.role.role_code === 'LIAISON')
        }
      }
    },
    methods: {
      ...mapMutations(['toggleAddITAExamModal', 'toggleGenFinReport', 'toggleNonITAExamModal']),
      clickAddIndividual() {
        this.toggleNonITAExamModal(false)
        this.toggleAddITAExamModal({visible: true, setup: 'individual'})
      },
      clickAddGroup() {
        this.toggleNonITAExamModal(false)
        this.toggleAddITAExamModal({visible: true, setup: 'group'})
      },
      clickGenFinReport() {
        this.toggleGenFinReport(true)
      },
      clickAddNonITA() {
        this.toggleNonITAExamModal(true)
        this.toggleAddITAExamModal({visible: true, setup: 'individual'})
      }
    }
  }
</script>
