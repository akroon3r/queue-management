<template>
  <b-form>
    <b-row no-gutters>
      <b-col cols="12">
        <span style="font-size:1rem">Please Review the Details You have Entered</span>
      </b-col>
    </b-row>
    <b-row v-if="errors.length > 0">
      <b-col cols="12">
        <span style="font-size:1rem; color: red">{{ submitMsg }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters class="mt-2" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Type</span>
      </b-col>
      <b-col>
        <span :style="{color: exam_object.exam_color}">
          {{ exam_object.exam_type_name }}
        </span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'group'">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Office</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ officeName }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="start" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Event ID</span>
      </b-col>
      <b-col>
        <span class="confirm-item">{{ exam.event_id }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="end" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Name</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.exam_name }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'individual'">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Writer's Name</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.examinee_name }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'group'">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Students</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.number_of_students }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'individual'">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Received Date</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.exam_received_date }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">{{ setup === 'group' ? 'Exam Date' : 'Expiry Date' }}</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ formatDate(exam.expiry_date) }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'group' ">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Time
        </span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ displayTime }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'group' ">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Location
        </span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.offsite_location }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Method</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.exam_method }}</span>
      </b-col>
    </b-row>
  </b-form>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import moment from 'moment'

  export default {
    name: "AddExamFormConfirm",
    props: ['submitMsg'],
    computed: {
      ...mapState({
        exam: state => state.capturedExam,
        examTypes: state => state.examTypes,
        tab: state => state.captureITAExamTabSetup,
        user: state => state.user,
        addITAExamModal: state => state.addITAExamModal,
        offices: state => state.offices,
      }),
      ...mapGetters(['exam_object']),
      officeName() {
        if (this.addITAExamModal.setup === 'group' && this.exam.office_id) {
          let office = this.offices.find(o => o.office_id == this.exam.office_id)
          return `#${office.office_id} - ${office.office_name}`
        }
        return ''
      },
      setup() {
        if (this.addITAExamModal.setup === 'individual') {
          return 'individual'
        }
        if (this.addITAExamModal.setup === 'group') {
          return 'group'
        }
      },
      errors() {
        if (this.tab.errors) {
          return this.tab.errors
        } else {
          this.submitMsg = ''
          return []
        }
      },
      displayTime() {
        if (this.exam && this.exam.exam_time) {
          return new moment(this.exam.exam_time).format('h:mm a')
        }
        return ''
      },
    },
    methods: {
      formatDate(d) {
        return new moment(d).format('MMM D, YYYY')
      }
    }
  }
</script>

<style scoped>
  .confirm-item {
    font-weight: 500; font-size: 1.05rem;
  }

</style>
